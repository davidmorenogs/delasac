# DELASAC Daily Infographic — Guía de instalación

## Estructura del proyecto

```
dailytech/
├── index.html                  ← Landing page
├── requirements.txt
├── .gitignore
├── infographics/
│   ├── manifest.json           ← Índice de infográficos (auto-generado)
│   └── YYYY-MM-DD-titulo.svg   ← Infográficos (auto-generados)
└── scripts/
    └── generate_infographic.py ← Script principal
```

---

## PASO 1 — Crear el repositorio en GitHub

1. Ve a [github.com](https://github.com) → **New repository**
2. Nombre: `dailytech` (o el que quieras)
3. Visibilidad: **Public** (necesario para Vercel gratis)
4. Crea sin README ni .gitignore (ya los tienes)

---

## PASO 2 — Subir el proyecto

En tu terminal, desde la carpeta del proyecto:

```bash
cd dailytech
git init
git add .
git commit -m "inicial: landing page + scripts"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/dailytech.git
git push -u origin main
```

---

## PASO 3 — Desplegar en Vercel (gratis)

1. Ve a [vercel.com](https://vercel.com) → **Add New Project**
2. Importa tu repositorio `dailytech` de GitHub
3. En **Framework Preset** selecciona **Other** (es HTML estático)
4. En **Root Directory** deja `/`
5. Haz clic en **Deploy**

Vercel te dará una URL como `https://dailytech-tuusuario.vercel.app`

Cada vez que hagas `git push`, Vercel redesplegará automáticamente en ~30s.

---

## PASO 4 — Configurar Python

En tu máquina local:

```bash
# Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate       # Mac/Linux
# venv\Scripts\activate        # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## PASO 5 — Obtener tu API Key de Anthropic

1. Ve a [console.anthropic.com](https://console.anthropic.com)
2. **API Keys** → **Create Key**
3. Copia la clave

Guárdala en tu sistema (elige UNO de estos métodos):

**Opción A — Variable de entorno permanente (Mac/Linux):**
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
source ~/.zshrc
```

**Opción B — Archivo .env en el proyecto:**
```bash
echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env
```
Y añade al inicio del script: `from dotenv import load_dotenv; load_dotenv()`
(también instala: `pip install python-dotenv`)

---

## PASO 6 — Uso diario (2 minutos)

### Rutina cada día:

1. **Haz tu resumen** en papel como siempre
2. **Fotografía el papel** con el móvil (buena luz, papel plano)
3. **Digitaliza el resumen** (escanea o fotografía la versión final)
4. **Ejecuta el script:**

```bash
# Desde la carpeta del proyecto:
./update-daily.sh ~/Desktop/photo.jpg ~/Desktop/scan.png "https://youtu.be/VIDEO_ID"
```

Eso es todo. En ~30 segundos:
- Crea carpeta del día
- Copia photo.jpg y scan.png
- Actualiza el manifest
- Hace `git push`
- Vercel redespliega

---

## Opciones del script

```bash
# Ejemplo con rutas completas
./update-daily.sh /Users/tu_usuario/Downloads/photo.jpg /Users/tu_usuario/Downloads/scan.png "https://youtu.be/abc123"

# Desde cualquier lugar
/Users/da_mo/Desktop/6.\ CONTENT/13.\ LANDING\ PAGE/update-daily.sh ~/Downloads/photo.jpg ~/Downloads/scan.png "https://youtu.be/abc123"
```

---

## PASO 7 (opcional) — Automatizar con un alias

Para que solo tengas que escribir `update-daily`:

```bash
# Añade a ~/.zshrc o ~/.bashrc:
alias update-daily='cd "/Users/da_mo/Desktop/6. CONTENT/13. LANDING PAGE" && ./update-daily.sh'
```

---

## Coste estimado

| Uso | Coste API |
|-----|-----------|
| 1 infográfico/día | ~0.01–0.02€ |
| 30 días/mes | ~0.30–0.60€ |

Vercel, GitHub: **gratis** en el plan gratuito.

---

## Solución de problemas frecuentes

**Error: `ANTHROPIC_API_KEY` no encontrada**
→ Comprueba que la variable de entorno está configurada: `echo $ANTHROPIC_API_KEY`

**El SVG no se ve en la web**
→ Asegúrate de que el `git push` fue exitoso: `git log --oneline -3`

**La imagen no se procesa bien**
→ Mejor iluminación, papel más plano, evitar sombras. El script funciona mejor con fotos nítidas.

**Vercel no redespliega**
→ Ve a vercel.com → tu proyecto → Deployments y comprueba si hay algún error.
