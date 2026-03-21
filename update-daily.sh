#!/bin/bash

# ═══════════════════════════════════════════════════════════════════
# DELASAC Daily Updater — Actualiza la web con el infográfico del día
# ═══════════════════════════════════════════════════════════════════
# Uso: ./update-daily.sh photo.jpg scan.png "https://youtu.be/VIDEO_ID"
# ═══════════════════════════════════════════════════════════════════

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Validar argumentos
if [ $# -ne 3 ]; then
  echo -e "${RED}❌ Error: Se requieren 3 argumentos${NC}"
  echo ""
  echo -e "${BLUE}Uso:${NC} ./update-daily.sh <photo.jpg> <scan.png> <video_url>"
  echo ""
  echo -e "${YELLOW}Ejemplo:${NC}"
  echo "  ./update-daily.sh photo.jpg scan.png \"https://youtu.be/abc123def456\""
  exit 1
fi

PHOTO="$1"
SCAN="$2"
VIDEO_URL="$3"

# Validar que los archivos existan
if [ ! -f "$PHOTO" ]; then
  echo -e "${RED}❌ Error: No se encontró foto: $PHOTO${NC}"
  exit 1
fi

if [ ! -f "$SCAN" ]; then
  echo -e "${RED}❌ Error: No se encontró scan: $SCAN${NC}"
  exit 1
fi

# Obtener la fecha de hoy (YYYY-MM-DD)
TODAY=$(date +%Y-%m-%d)
INFOGRAPHIC_DIR="./infographics/$TODAY"

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🚀 DELASAC Daily Updater${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📅 Fecha:${NC} $TODAY"
echo -e "${YELLOW}📸 Foto:${NC} $PHOTO"
echo -e "${YELLOW}📄 Scan:${NC} $SCAN"
echo -e "${YELLOW}🎬 Video:${NC} $VIDEO_URL"
echo ""

# Paso 1: Crear carpeta del día
echo -e "${BLUE}[1/5]${NC} Creando carpeta: $INFOGRAPHIC_DIR"
mkdir -p "$INFOGRAPHIC_DIR"
if [ $? -ne 0 ]; then
  echo -e "${RED}❌ Error al crear carpeta${NC}"
  exit 1
fi
echo -e "${GREEN}✅ Carpeta creada${NC}"
echo ""

# Paso 2: Copiar archivos
echo -e "${BLUE}[2/5]${NC} Copiando archivos..."
cp "$PHOTO" "$INFOGRAPHIC_DIR/photo.jpg"
if [ $? -ne 0 ]; then
  echo -e "${RED}❌ Error al copiar foto${NC}"
  exit 1
fi
echo -e "${GREEN}✅ Foto copiada${NC}"

cp "$SCAN" "$INFOGRAPHIC_DIR/scan.png"
if [ $? -ne 0 ]; then
  echo -e "${RED}❌ Error al copiar scan${NC}"
  exit 1
fi
echo -e "${GREEN}✅ Scan copiado${NC}"
echo ""

# Paso 3: Buscar SVG en la carpeta del día
echo -e "${BLUE}[3/5]${NC} Buscando SVG en Desktop..."
SVG_FILE=$(find ~/Desktop -name "*.svg" -type f -mmin -60 2>/dev/null | head -1)

if [ -z "$SVG_FILE" ]; then
  echo -e "${YELLOW}⚠️  No se encontró SVG reciente en Desktop${NC}"
  echo -e "${YELLOW}ℹ️  Si tienes un SVG, cópialo manualmente a: $INFOGRAPHIC_DIR/${NC}"
else
  cp "$SVG_FILE" "$INFOGRAPHIC_DIR/$(basename $SVG_FILE)"
  echo -e "${GREEN}✅ SVG copiado: $(basename $SVG_FILE)${NC}"
fi
echo ""

# Paso 4: Actualizar manifest.json
echo -e "${BLUE}[4/5]${NC} Actualizando manifest.json..."

# Contar items (líneas del SVG si existe, si no usar 0)
if [ -n "$SVG_FILE" ]; then
  ITEMS=$(grep -c "<text" "$SVG_FILE" 2>/dev/null || echo "0")
else
  ITEMS="0"
fi

# Encontrar el SVG que acabamos de copiar
SVG_BASENAME=$(ls "$INFOGRAPHIC_DIR"/*.svg 2>/dev/null | xargs -n1 basename | head -1)
SVG_PATH="infographics/$TODAY/$SVG_BASENAME"

if [ -z "$SVG_BASENAME" ]; then
  SVG_PATH="infographics/$TODAY/infogr.svg"
fi

# Crear/actualizar manifest.json con la entrada del día
MANIFEST="./infographics/manifest.json"

# Crear JSON entry
JSON_ENTRY="{
  \"date\": \"$TODAY\",
  \"title\": \"TECH BRIEF - $(date +%B | tr a-z A-Z) $(date +%Y)\",
  \"items\": $ITEMS,
  \"photo\": \"infographics/$TODAY/photo.jpg\",
  \"scan\": \"infographics/$TODAY/scan.png\",
  \"svg\": \"$SVG_PATH\",
  \"videoUrl\": \"$VIDEO_URL\"
}"

# Si manifest no existe, criar como array
if [ ! -f "$MANIFEST" ]; then
  echo "[$JSON_ENTRY]" > "$MANIFEST"
  echo -e "${GREEN}✅ Manifest creado${NC}"
else
  # Agregar entrada nueva (simple: reemplaza el penúltimo carácter ] con nueva entry)
  # Esto es básico pero funciona para este caso
  temp=$(mktemp)
  head -n -1 "$MANIFEST" > "$temp"
  echo ",$JSON_ENTRY" >> "$temp"
  echo "]" >> "$temp"
  mv "$temp" "$MANIFEST"
  echo -e "${GREEN}✅ Manifest actualizado${NC}"
fi
echo ""

# Paso 5: Git push
echo -e "${BLUE}[5/5]${NC} Publicando a GitHub..."
git add .
if [ $? -ne 0 ]; then
  echo -e "${RED}❌ Error en git add${NC}"
  exit 1
fi

git commit -m "Update: DELASAC daily infographic for $TODAY"
if [ $? -ne 0 ]; then
  echo -e "${RED}❌ Error en git commit${NC}"
  exit 1
fi

git push
if [ $? -ne 0 ]; then
  echo -e "${RED}❌ Error en git push${NC}"
  exit 1
fi
echo -e "${GREEN}✅ Publicado en GitHub${NC}"
echo ""

# Resumen final
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ ¡COMPLETADO! La web se actualizará en ~30 segundos${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📍 Ubicación de archivos:${NC}"
echo "   $INFOGRAPHIC_DIR/"
echo "   ├── photo.jpg"
echo "   ├── scan.png"
echo "   └── $([ -n "$SVG_BASENAME" ] && echo "$SVG_BASENAME" || echo "*.svg (manual)")"
echo ""
echo -e "${YELLOW}🌐 Web actualizada en:${NC}"
echo "   https://delasac.com"
echo ""
