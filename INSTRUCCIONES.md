# DELASAC Daily Infographic — Guía de uso v2

## Estructura del proyecto (actualizada)

```
dailytech/
├── index.html                           ← Landing page responsiva
├── scripts/
│   └── generate_infographic.py          ← Script principal
├── infographics/
│   ├── manifest.json                    ← Índice de infográficos (auto-generado)
│   ├── 2026-03-20/
│   │   ├── photo.jpg                    ← Foto original manuscrita (jpg)
│   │   ├── scan.png                     ← Escaneo digitalizado
│   │   └── 2026-03-20-tech-brief-marzo-2026.svg  ← Infográfico generado
│   ├── 2026-03-21/
│   │   ├── photo.jpg
│   │   ├── scan.png
│   │   └── ...
└── requirements.txt
```

## Uso del script

### Sintaxis básica

```bash
python scripts/generate_infographic.py <foto_para_extraer> --photo <original.HEIC> --scan <scan.png> [opciones]
```

### Parámetros

- `<foto_para_extraer>`: Imagen para extraer contenido (puede ser la misma que `--photo`)
- `--photo`: Ruta a la foto original manuscrita (JPG, PNG, HEIC)* 
- `--scan`: Ruta al escaneo digitalizado (PNG, JPG)
- `--video`: (Opcional) URL del video de YouTube (ej: `https://youtu.be/TC_doATsgJY?si=...`)
- `--date`: (Opcional) Fecha YYYY-MM-DD (por defecto: hoy)
- `--no-push`: (Opcional) Solo genera localmente, no publica en GitHub

*HEIC se convierte automáticamente a JPG

### Ejemplos

**Generación básica (sin publicar)**
```bash
python scripts/generate_infographic.py photo.jpg --photo photo.jpg --scan scan.png --no-push
```

**Con video de YouTube**
```bash
python scripts/generate_infographic.py photo.jpg \
  --photo photo.jpg \
  --scan scan.png \
  --video "https://youtu.be/TC_doATsgJY?si=rzgGUH4hp73FfqSQ" \
  --no-push
```

**Con fecha personalizada**
```bash
python scripts/generate_infographic.py photo.jpg \
  --photo photo.jpg \
  --scan scan.png \
  --date 2026-03-25 \
  --no-push
```

**Publicar en GitHub (con auto-redeploy en Vercel)**
```bash
python scripts/generate_infographic.py photo.jpg \
  --photo photo.jpg \
  --scan scan.png \
  --video "https://youtu.be/TC_doATsgJY?si=rzgGUH4hp73FfqSQ"
```

## Estructura del manifest.json

```json
[
  {
    "date": "2026-03-20",
    "title": "TECH BRIEF - MARZO 2026",
    "items": 4,
    "photo": "infographics/2026-03-20/photo.jpg",
    "scan": "infographics/2026-03-20/scan.png",
    "svg": "infographics/2026-03-20/2026-03-20-tech-brief-marzo-2026.svg",
    "videoUrl": "https://youtu.be/TC_doATsgJY?si=rzgGUH4hp73FfqSQ"
  }
]
```

## Layout de la web

### Desktop (≥ 501px)
- **Featured**: Lado-a-lado (Izq: original, Dcha: scan)
- **Video**: Embed de YouTube + links
- **Archive**: Grid de thumbnails

### Mobile (≤ 500px)
- **Featured**: Apilado verticalmente (Original arriba, Scan abajo)
- **Video**: Responsivo
- **Archive**: Grid de 2 columnas

## Deployment en Vercel

1. Pushea los cambios a GitHub
2. Vercel redesplegará automáticamente en ~30 segundos
3. La web se actualiza mostrando el último infográfico

## Notas

- Los archivos se organizan automáticamente por fecha (carpeta YYYY-MM-DD)
- El manifest.json se ordena por fecha descendente (más reciente primero)
- La foto original y el escaneo se muestran lado-a-lado en desktop, apilados en mobile
- El video de YouTube se embebe con controles completos
- El archivo .env contiene ANTHROPIC_API_KEY para Claude Vision
