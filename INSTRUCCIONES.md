# DELASAC Daily Infographic — Guía de uso v2

## Estructura del proyecto (actualizada)

```
dailytech/
├── index.html                           ← Landing page responsiva
├── update-daily.sh                      ← Script principal
├── infographics/
│   ├── manifest.json                    ← Índice de infográficos
│   ├── 2026-03-20/
│   │   ├── photo.jpg                    ← Foto original manuscrita
│   │   └── scan.png                     ← Escaneo digitalizado
│   ├── 2026-03-21/
│   │   ├── photo.jpg
│   │   └── scan.png
│   └── ...
└── requirements.txt
```

## Uso del script

### Sintaxis básica

```bash
./update-daily.sh <photo.jpg> <scan.png> "<video_url>"
```

### Parámetros

- `photo.jpg`: Ruta a la foto original manuscrita
- `scan.png`: Ruta al escaneo digitalizado
- `video_url`: URL completa de YouTube (ej: `https://youtu.be/abc123def456`)

### Ejemplos

**Desde la carpeta del proyecto**
```bash
cd "/Users/da_mo/Desktop/6. CONTENT/13. LANDING PAGE"
./update-daily.sh ~/Downloads/photo.jpg ~/Downloads/scan.png "https://youtu.be/abc123def456"
```

**Con rutas completas**
```bash
./update-daily.sh /Users/davidmorenogs/Downloads/photo.jpg /Users/davidmorenogs/Downloads/scan.png "https://youtu.be/jAYtP8ZJRPc"
```

## Estructura del manifest.json

```json
[
  {
    "date": "2026-03-24",
    "title": "TECH BRIEF - MARCH 2026",
    "items": 0,
    "photo": "infographics/2026-03-24/photo.jpg",
    "scan": "infographics/2026-03-24/scan.png",
    "svg": "",
    "videoUrl": "https://youtu.be/abc123def456"
  }
]
```

**Campos:**
- `date`: Fecha YYYY-MM-DD
- `title`: Título del día (generado automáticamente)
- `items`: Contador de items (actualmente no usado)
- `photo`: Ruta a la foto original
- `scan`: Ruta al escaneo (mostrado como miniatura en el archivo)
- `svg`: Campo vacío (no se genera automáticamente)
- `videoUrl`: URL de YouTube

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
- El scan.png se usa como miniatura en el historial de días anteriores
- El video de YouTube se embebe con controles completos
- **NO se genera SVG automáticamente** — solo copia y organiza archivos existentes
