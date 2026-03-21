#!/usr/bin/env python3
"""
generate_infographic.py v2
────────────────────────────────────────────────────────────────────────────
Flujo completo:
  1. Lee una imagen (foto del papel de notas diario)
  2. La manda a Claude Vision API → extrae titulo + items estructurados
  3. Genera un SVG infográfico adaptado a móvil
  4. Organiza archivos en carpeta por fecha: photo + scan + svg
  5. Actualiza manifest.json con referencias a las tres versiones
  6. Git add + commit + push → Vercel redeploy automático

Uso:
  python generate_infographic.py paper_photo.jpg --photo original.HEIC --scan scan.png
  python generate_infographic.py paper_photo.jpg --photo original.HEIC --scan scan.png --date 2025-03-20
  python generate_infographic.py paper_photo.jpg --photo original.HEIC --scan scan.png --video "https://youtu.be/..."
  python generate_infographic.py paper_photo.jpg --photo original.HEIC --scan scan.png --no-push
"""

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path
import anthropic

# ── CONFIGURACIÓN ────────────────────────────────────────────────────────────
INFOGRAPHICS_DIR = Path(__file__).parent.parent / "infographics"
MANIFEST_FILE    = INFOGRAPHICS_DIR / "manifest.json"
SVG_WIDTH        = 390   # px — ancho estándar móvil
MAX_ITEMS        = 8     # máximo de noticias por infográfico

# Paleta (debe coincidir con index.html)
COLORS = {
    "bg":       "#FFFFFF",
    "surface":  "#F5F3EE",
    "border":   "#C8C5BC",
    "text":     "#1A1814",
    "muted":    "#7A776F",
    "accent":   "#0A5FFF",
    "tag_bg":   "#EFF3FF",
    "tag_text": "#0A5FFF",
}

# ── HELPERS ──────────────────────────────────────────────────────────────────

def encode_image(path: str) -> tuple[str, str]:
    """Devuelve (base64_data, media_type)."""
    ext = Path(path).suffix.lower()
    media_types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                   ".png": "image/png",  ".webp": "image/webp",
                   ".gif": "image/gif"}
    media_type = media_types.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8"), media_type


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[áàä]", "a", text)
    text = re.sub(r"[éèë]", "e", text)
    text = re.sub(r"[íìï]", "i", text)
    text = re.sub(r"[óòö]", "o", text)
    text = re.sub(r"[úùü]", "u", text)
    text = re.sub(r"ñ", "n", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:60]


def wrap_text(text: str, max_chars: int) -> list[str]:
    """Divide texto en líneas respetando palabras."""
    return textwrap.wrap(text, width=max_chars) or [""]


# ── 1. EXTRACCIÓN VÍA CLAUDE VISION ─────────────────────────────────────────

EXTRACTION_PROMPT = """\
Analiza esta imagen de un papel de notas con resumen de noticias tecnológicas.

Extrae la información y devuelve ÚNICAMENTE un JSON válido con esta estructura exacta:

{
  "title": "Título breve del día (máx 50 caracteres)",
  "subtitle": "Subtítulo o fecha si aparece (puede ser vacío)",
  "items": [
    {
      "category": "Categoría corta (IA, Espacio, Defensa, Semiconductores, etc.)",
      "headline": "Titular principal de la noticia (máx 80 caracteres)",
      "detail": "Detalle o dato clave adicional (máx 120 caracteres, puede ser vacío)",
      "has_diagram": false
    }
  ],
  "diagrams": [
    {
      "description": "Descripción del diagrama o esquema visual que aparece en el papel"
    }
  ],
  "notes": "Cualquier nota o reflexión adicional que aparezca (puede ser vacío)"
}

Reglas:
- Máximo 8 items
- Si hay diagramas, flechas o esquemas visuales en el papel, descríbelos en "diagrams"
- Trunca textos largos con "..." si superan el límite
- No incluyas texto fuera del JSON
- Si el papel está en español, mantén el contenido en español
"""

def extract_content(image_path: str) -> dict:
    """Manda la imagen a Claude y obtiene JSON estructurado."""
    print(f"  → Enviando imagen a Claude Vision...")
    
    client = anthropic.Anthropic()  # usa ANTHROPIC_API_KEY del entorno
    img_data, media_type = encode_image(image_path)

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1500,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": img_data,
                        },
                    },
                    {"type": "text", "text": EXTRACTION_PROMPT},
                ],
            }
        ],
    )

    raw = message.content[0].text.strip()
    # Limpiar posibles backticks de markdown
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  ✗ Error parseando JSON: {e}")
        print(f"  Respuesta raw:\n{raw[:500]}")
        sys.exit(1)

    return data


# ── 2. GENERACIÓN DEL SVG ────────────────────────────────────────────────────

def make_category_tag_svg(x, y, category, color=None):
    """Genera SVG para una etiqueta de categoría."""
    c = color or COLORS["accent"]
    bg = COLORS["tag_bg"]
    return f'''
    <rect x="{x}" y="{y}" width="auto" rx="3" fill="{bg}"/>
    <text x="{x+6}" y="{y+11}" font-family="'IBM Plex Mono',monospace"
          font-size="9" font-weight="500" fill="{c}">{category[:20]}</text>
    '''


def estimate_tag_width(text: str) -> int:
    return min(len(text) * 6.5 + 12, 100)


def generate_svg(data: dict, date_str: str) -> str:
    """Genera el SVG completo del infográfico."""
    items    = data.get("items", [])[:MAX_ITEMS]
    title    = data.get("title", "Tech Brief")
    subtitle = data.get("subtitle", "")
    notes    = data.get("notes", "")
    diagrams = data.get("diagrams", [])
    
    # Formato de fecha
    dt = datetime.fromisoformat(date_str)
    date_display = dt.strftime("%-d %b %Y").upper()
    day_display  = dt.strftime("%A").upper()

    # Calcular altura dinámica
    HEADER_H  = 110
    ITEM_H    = 82   # altura base por item
    NOTES_H   = 60 if notes else 0
    DIAGRAM_H = 70 * len(diagrams)
    FOOTER_H  = 44
    PAD_V     = 20
    
    # Ajuste de altura por items con detalle largo
    items_height = 0
    for item in items:
        lines_headline = len(wrap_text(item.get("headline",""), 42))
        lines_detail   = len(wrap_text(item.get("detail",""), 50)) if item.get("detail") else 0
        items_height  += 52 + lines_headline * 16 + lines_detail * 14

    total_h = HEADER_H + items_height + NOTES_H + DIAGRAM_H + FOOTER_H + PAD_V * 2
    W = SVG_WIDTH
    PAD = 20

    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {total_h}"
     font-family="'IBM Plex Sans','Helvetica Neue',sans-serif">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&amp;family=IBM+Plex+Sans:wght@300;400;500&amp;display=swap');
    </style>
  </defs>
''')

    # ── FONDO ────────────────────────────────────────────────────
    svg_parts.append(f'  <rect width="{W}" height="{total_h}" fill="{COLORS["bg"]}"/>')
    svg_parts.append(f'  <rect width="{W}" height="{HEADER_H}" fill="{COLORS["surface"]}"/>')
    svg_parts.append(f'  <line x1="0" y1="{HEADER_H}" x2="{W}" y2="{HEADER_H}" stroke="{COLORS["border"]}" stroke-width="1"/>')

    # ── HEADER ───────────────────────────────────────────────────
    # Día de la semana
    svg_parts.append(f'''  <text x="{PAD}" y="26"
    font-family="'IBM Plex Mono',monospace"
    font-size="9" font-weight="500" letter-spacing="2"
    fill="{COLORS["accent"]}" text-anchor="start">{day_display} · TECH BRIEF</text>''')

    # Título principal
    title_lines = wrap_text(title, 28)
    for i, line in enumerate(title_lines[:2]):
        svg_parts.append(f'''  <text x="{PAD}" y="{50 + i*28}"
    font-family="'IBM Plex Mono',monospace"
    font-size="24" font-weight="600" letter-spacing="-0.5"
    fill="{COLORS["text"]}">{line}</text>''')

    # Fecha (derecha)
    svg_parts.append(f'''  <text x="{W - PAD}" y="26"
    font-family="'IBM Plex Mono',monospace"
    font-size="9" fill="{COLORS["muted"]}"
    text-anchor="end">{date_display}</text>''')

    # Subtítulo
    if subtitle:
        svg_parts.append(f'''  <text x="{PAD}" y="{HEADER_H - 16}"
    font-family="'IBM Plex Sans',sans-serif"
    font-size="11" font-weight="300"
    fill="{COLORS["muted"]}">{subtitle[:60]}</text>''')

    # Línea decorativa accent
    svg_parts.append(f'  <rect x="{PAD}" y="{HEADER_H - 4}" width="32" height="2" fill="{COLORS["accent"]}" rx="1"/>')

    # ── ITEMS ─────────────────────────────────────────────────────
    y = HEADER_H + PAD_V

    for idx, item in enumerate(items):
        category = item.get("category", "")
        headline = item.get("headline", "")
        detail   = item.get("detail", "")

        headline_lines = wrap_text(headline, 42)
        detail_lines   = wrap_text(detail, 50) if detail else []

        # Separador entre items
        if idx > 0:
            svg_parts.append(f'  <line x1="{PAD}" y1="{y}" x2="{W-PAD}" y2="{y}" stroke="{COLORS["border"]}" stroke-width="0.5" stroke-dasharray="3,3"/>')
            y += 12

        # Número del item
        svg_parts.append(f'''  <text x="{PAD}" y="{y+15}"
    font-family="'IBM Plex Mono',monospace"
    font-size="9" fill="{COLORS["border"]}">{str(idx+1).zfill(2)}</text>''')

        # Tag de categoría
        tag_w = estimate_tag_width(category)
        svg_parts.append(f'  <rect x="{PAD+22}" y="{y+3}" width="{tag_w}" height="15" rx="2" fill="{COLORS["tag_bg"]}"/>')
        svg_parts.append(f'''  <text x="{PAD+28}" y="{y+14}"
    font-family="'IBM Plex Mono',monospace"
    font-size="8.5" font-weight="500"
    fill="{COLORS["accent"]}">{category[:20]}</text>''')

        y += 24

        # Titular
        for line in headline_lines:
            svg_parts.append(f'''  <text x="{PAD}" y="{y}"
    font-family="'IBM Plex Sans',sans-serif"
    font-size="13.5" font-weight="500"
    fill="{COLORS["text"]}">{line}</text>''')
            y += 17

        # Detalle
        if detail_lines:
            y += 2
            for line in detail_lines:
                svg_parts.append(f'''  <text x="{PAD}" y="{y}"
    font-family="'IBM Plex Sans',sans-serif"
    font-size="11" font-weight="300"
    fill="{COLORS["muted"]}">{line}</text>''')
                y += 14

        y += 10

    # ── DIAGRAMAS (si los hay) ────────────────────────────────────
    if diagrams:
        y += 8
        svg_parts.append(f'  <line x1="{PAD}" y1="{y}" x2="{W-PAD}" y2="{y}" stroke="{COLORS["border"]}" stroke-width="1"/>')
        y += 14
        svg_parts.append(f'''  <text x="{PAD}" y="{y}"
    font-family="'IBM Plex Mono',monospace"
    font-size="8.5" font-weight="500" letter-spacing="1.5"
    fill="{COLORS["muted"]}">ESQUEMAS DETECTADOS</text>''')
        y += 14

        for diag in diagrams:
            desc = diag.get("description", "")
            desc_lines = wrap_text(desc, 52)
            # Caja de diagrama
            box_h = 14 * len(desc_lines) + 20
            svg_parts.append(f'  <rect x="{PAD}" y="{y}" width="{W-PAD*2}" height="{box_h}" rx="4" fill="{COLORS["surface"]}" stroke="{COLORS["border"]}" stroke-width="1"/>')
            svg_parts.append(f'''  <text x="{PAD+10}" y="{y+12}"
    font-family="'IBM Plex Mono',monospace"
    font-size="8" fill="{COLORS["accent"]}">◈ ESQUEMA</text>''')
            for i, line in enumerate(desc_lines):
                svg_parts.append(f'''  <text x="{PAD+10}" y="{y+26+i*14}"
    font-family="'IBM Plex Sans',sans-serif"
    font-size="10.5" font-weight="300"
    fill="{COLORS["muted"]}">{line}</text>''')
            y += box_h + 10

    # ── NOTAS ─────────────────────────────────────────────────────
    if notes:
        y += 8
        note_lines = wrap_text(notes, 50)
        svg_parts.append(f'  <rect x="{PAD}" y="{y}" width="3" height="{14*len(note_lines)+4}" fill="{COLORS["accent"]}" rx="1"/>')
        for i, line in enumerate(note_lines):
            svg_parts.append(f'''  <text x="{PAD+12}" y="{y+13+i*14}"
    font-family="'IBM Plex Sans',sans-serif"
    font-size="11" font-style="italic"
    fill="{COLORS["muted"]}">{line}</text>''')
        y += 14 * len(note_lines) + 18

    # ── FOOTER ────────────────────────────────────────────────────
    footer_y = total_h - FOOTER_H + 10
    svg_parts.append(f'  <line x1="0" y1="{footer_y-8}" x2="{W}" y2="{footer_y-8}" stroke="{COLORS["border"]}" stroke-width="0.5"/>')
    svg_parts.append(f'''  <text x="{PAD}" y="{footer_y+6}"
    font-family="'IBM Plex Mono',monospace"
    font-size="8.5" fill="{COLORS["muted"]}">DELASAC · delasac.com</text>''')
    svg_parts.append(f'''  <text x="{W-PAD}" y="{footer_y+6}"
    font-family="'IBM Plex Mono',monospace"
    font-size="8.5" fill="{COLORS["border"]}"
    text-anchor="end">{len(items)} TEMAS</text>''')

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


# ── 3. ACTUALIZAR MANIFEST ───────────────────────────────────────────────────

def update_manifest(date_str: str, title: str, svg_filename: str, n_items: int,
                   photo_path: str = None, scan_path: str = None, video_url: str = None):
    """Añade o actualiza la entrada del día en manifest.json."""
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE, "r") as f:
            manifest = json.load(f)
    else:
        manifest = []

    # Eliminar entrada del mismo día si existe
    manifest = [e for e in manifest if e.get("date") != date_str]

    day_dir = f"infographics/{date_str}"
    entry = {
        "date":  date_str,
        "title": title,
        "items": n_items,
        "svg":   f"{day_dir}/{svg_filename}",
    }
    
    # Añadir rutas de photo y scan si existen
    if photo_path:
        entry["photo"] = photo_path
    if scan_path:
        entry["scan"] = scan_path
    if video_url:
        entry["videoUrl"] = video_url

    manifest.append(entry)

    # Ordenar por fecha descendente
    manifest.sort(key=lambda e: e["date"], reverse=True)

    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"  → manifest.json actualizado ({len(manifest)} entradas)")


# ── 4. GIT PUSH ──────────────────────────────────────────────────────────────

def git_push(date_str: str, svg_path: Path):
    """Hace git add + commit + push."""
    print("  → Publicando en GitHub...")
    
    # Añadir toda la carpeta del día + manifest
    day_path = INFOGRAPHICS_DIR / date_str
    
    cmds = [
        ["git", "add", str(day_path), str(MANIFEST_FILE)],
        ["git", "commit", "-m", f"infographic: {date_str}"],
        ["git", "push"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True,
                                cwd=Path(__file__).parent.parent)
        if result.returncode != 0:
            print(f"  ✗ Error en {' '.join(cmd)}:")
            print(result.stderr)
            sys.exit(1)
    print("  ✓ Publicado. Vercel redesplegará en ~30 segundos.")


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Genera infográfico desde foto de papel + originales")
    parser.add_argument("image", help="Ruta a la imagen para extraer contenido (JPG/PNG/WEBP)")
    parser.add_argument("--photo", help="Ruta a la foto original (HEIC/JPG/PNG)")
    parser.add_argument("--scan", help="Ruta al escaneo digital (PNG/JPG)")
    parser.add_argument("--video", help="URL del video de YouTube (opcional)")
    parser.add_argument("--date", default=datetime.today().strftime("%Y-%m-%d"),
                        help="Fecha YYYY-MM-DD (por defecto: hoy)")
    parser.add_argument("--no-push", action="store_true",
                        help="Solo genera, no publica en GitHub")
    args = parser.parse_args()

    if not Path(args.image).exists():
        print(f"✗ No se encuentra la imagen: {args.image}")
        sys.exit(1)

    if args.photo and not Path(args.photo).exists():
        print(f"✗ No se encuentra la foto: {args.photo}")
        sys.exit(1)

    if args.scan and not Path(args.scan).exists():
        print(f"✗ No se encuentra el scan: {args.scan}")
        sys.exit(1)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("✗ Falta la variable de entorno ANTHROPIC_API_KEY")
        sys.exit(1)

    INFOGRAPHICS_DIR.mkdir(exist_ok=True)
    
    # Crear carpeta del día
    day_dir = INFOGRAPHICS_DIR / args.date
    day_dir.mkdir(exist_ok=True)

    print(f"\n▸ Procesando: {args.image} [{args.date}]")
    if args.photo:
        print(f"  → Original: {args.photo}")
    if args.scan:
        print(f"  → Scan: {args.scan}")

    # Paso 1: Extracción
    print("\n[1/5] Extrayendo contenido con Claude Vision...")
    data = extract_content(args.image)
    title  = data.get("title", "Tech Brief")
    n_items = len(data.get("items", []))
    print(f"  ✓ Extraídos {n_items} items — «{title}»")

    # Paso 2: Generar SVG
    print("\n[2/5] Generando infográfico SVG...")
    svg_content  = generate_svg(data, args.date)
    svg_filename = f"{args.date}-{slugify(title)}.svg"
    svg_path     = day_dir / svg_filename
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"  ✓ SVG guardado: {svg_path}")

    # Paso 3: Copiar archivos originales
    photo_path_rel = None
    scan_path_rel = None
    
    if args.photo:
        print("\n[3/5] Copiando foto original...")
        photo_ext = Path(args.photo).suffix.lower()
        # Normalizar extensión: .heic → .jpg
        if photo_ext in ['.heic', '.heif']:
            photo_dest = day_dir / "photo.jpg"
        else:
            photo_dest = day_dir / f"photo{photo_ext}"
        shutil.copy(args.photo, photo_dest)
        photo_path_rel = f"infographics/{args.date}/{photo_dest.name}"
        print(f"  ✓ Foto copiada: {photo_dest}")

    if args.scan:
        print("\n[4/5] Copiando escaneo digital...")
        scan_ext = Path(args.scan).suffix
        scan_dest = day_dir / f"scan{scan_ext}"
        shutil.copy(args.scan, scan_dest)
        scan_path_rel = f"infographics/{args.date}/scan{scan_ext}"
        print(f"  ✓ Scan copiado: {scan_dest}")

    # Paso 5: Actualizar manifest
    print("\n[5/5] Actualizando manifest.json...")
    update_manifest(args.date, title, svg_filename, n_items,
                   photo_path=photo_path_rel, scan_path=scan_path_rel,
                   video_url=args.video)

    # Publicar
    if args.no_push:
        print("\n► Modo --no-push: omitiendo publicación.")
        print(f"\n✓ Listo. Abre index.html en tu navegador para ver el resultado.")
    else:
        print("\n► Publicando en GitHub → Vercel...")
        git_push(args.date, svg_path)
        print(f"\n✓ Todo publicado. Revisa tu web en unos 30 segundos.")


if __name__ == "__main__":
    main()
