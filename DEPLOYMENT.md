# DELASAC — Guía de Deployment

## Pasos para desplegar la web públicamente

### PASO 1: Preparar repositorio GitHub

#### 1.1 Crear repositorio en GitHub
1. Ve a [github.com](https://github.com)
2. Haz clic en **New repository** (o el ícono +)
3. Nombre: `delasac` (o el que prefieras)
4. Descripción: "Daily Tech Brief — Infographics"
5. **Public** (importante para Vercel gratis)
6. **NO** initializes with README (ya los tienes)
7. Haz clic en **Create repository**

#### 1.2 Vincular repositorio local a GitHub
```bash
cd "/Users/da_mo/Desktop/6. CONTENT/13. LANDING PAGE"

# Inicializar git (si no está)
git init

# Añadir todos los archivos
git add .

# Commit inicial
git commit -m "Initial commit: daily infographics landing page"

# Cambiar rama a main
git branch -M main

# Vincular al repositorio remoto (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/delasac.git

# Primero push
git push -u origin main
```

**Nota**: Si pide autenticación, crea un **Personal Access Token** en GitHub:
- [Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
- Genera uno con permisos `repo`
- Úsalo como contraseña en lugar de tu password

---

### PASO 2: Desplegar en Vercel (RECOMENDADO - Gratis y automático)

#### 2.1 Conectar Vercel a tu repositorio
1. Ve a [vercel.com](https://vercel.com)
2. Haz clic en **Sign Up** (con GitHub si prefieres)
3. Una vez en el dashboard, ve a **Add New Project**
4. Selecciona **Import Git Repository**
5. Busca tu repositorio `delasac`
6. Haz clic en **Import**

#### 2.2 Configurar el proyecto
En la pantalla de configuración:
- **Framework Preset**: `Other` (es HTML estático)
- **Root Directory**: `/` (raíz del proyecto)
- **Build Command**: dejar vacío
- **Output Directory**: `/`

#### 2.3 Desplegar
- Haz clic en **Deploy**
- Vercel mostrará un URL en el formato: `https://delasac-XXXXX.vercel.app`

---

### PASO 3: Auto-deploy automático

Una vez conectado Vercel a tu repositorio GitHub:

**Cada vez que hagas `git push`:**
1. Vercel detecta los cambios automáticamente
2. Redeploya la web en ~30-60 segundos
3. Los cambios están en vivo

**Ejemplo de flujo diario:**

```bash
# Día 21 de marzo (viernes)
cd "/Users/da_mo/Desktop/6. CONTENT/13. LANDING PAGE"

# Tienes photo.jpg, scan.png y video
python scripts/generate_infographic.py photo.jpg \
  --photo photo.jpg \
  --scan scan.png \
  --video "https://youtu.be/NEW_VIDEO_ID" \
  --no-push

# Verificar en navegador: index.html

# Si todo se ve bien, publicar (sin --no-push):
python scripts/generate_infographic.py photo.jpg \
  --photo photo.jpg \
  --scan scan.png \
  --video "https://youtu.be/NEW_VIDEO_ID"

# El script hace: git add, git commit, git push
# Vercel redeploya automáticamente
```

---

### PASO 4: Dominio personalizado (OPCIONAL)

Si quieres usar tu propio dominio (ej: `delasac.com`):

#### 4.1 Comprar dominio
- Proveedores: Namecheap, Google Domains, Cloudflare, etc.

#### 4.2 Configurar en Vercel
1. En Vercel dashboard, abre tu proyecto
2. Ve a **Settings → Domains**
3. Haz clic en **Add Domain**
4. Escribe tu dominio (ej: `delasac.com`)
5. Sigue las instrucciones para actualizar los DNS

#### 4.3 Apuntar registros DNS
Vercel te dará instrucciones específicas. Generalmente:
- **CNAME**: `www.delasac.com` → `cname.vercel-dns.com`
- **A Record**: `delasac.com` → IP de Vercel (varía)

---

### PASO 5: Optimizaciones finales

#### 5.1 Página personalizada de errores (Opcional)
Crea `public/404.html` para error pages customizadas

#### 5.2 Analytics (Opcional)
- Vercel tiene analytics integrado
- [Analytics en dashboard](https://vercel.com/docs/analytics)

#### 5.3 Environment variables
Si usas ANTHROPIC_API_KEY en producción:
1. Ve a **Settings → Environment Variables** en Vercel
2. Añade: `ANTHROPIC_API_KEY` = tu clave
3. No subas `.env` a GitHub por seguridad

---

### Resumen del comando para publicar cada día

```bash
ANTHROPIC_API_KEY="sk-ant-api..." python scripts/generate_infographic.py photo.jpg \
  --photo photo.jpg \
  --scan scan.png \
  --video "https://youtu.be/VIDEO_ID"
```

Final: Tu web estará en vivo en `https://delasac-XXXXX.vercel.app` (o tu dominio personalizado)

---

### Solución de problemas

**"git push rechazado"**
- Verifica que hayas hecho `git config user.name` y `git config user.email`
- Usa Personal Access Token de GitHub en lugar de password

**"Vercel no redeploya"**
- Espera 1-2 minutos después del push
- Verifica que el repositorio esté conectado correctamente
- Revisa los logs en Vercel dashboard

**"Imágenes no se cargan"**
- Revisa que las rutas en `manifest.json` sean correctas
- Los archivos deben estar en la carpeta `infographics/YYYY-MM-DD/`

**"Video de YouTube no se muestra"**
- La URL debe ser válida y pública
- Vercel cacheará la miniatura
- Prueba con `--no-push` primero

---

### Monitoreo

Una vez en vivo, puedes:
- Ver logs en Vercel dashboard
- Monitorear performance
- Revisar analytics
- Recibir notificaciones de errores

¡Listo para publicar! 🚀
