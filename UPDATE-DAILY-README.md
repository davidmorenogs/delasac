# 🚀 DELASAC Daily Updater Script

Script automatizado para actualizar delasac.com cada día con el nuevo infográfico.

---

## 📋 **Qué hace el script**

El script `update-daily.sh` automáticamente:
1. ✅ Crea carpeta `/infographics/YYYY-MM-DD/` con la fecha del día
2. ✅ Copia tu foto original (`photo.jpg`)
3. ✅ Copia tu escaneo (`scan.png`)
4. ✅ Actualiza `manifest.json` con todos los datos
5. ✅ Hace `git push` a GitHub
6. ✅ **Vercel redeploya automáticamente en ~30 segundos**

---

## 🎯 **Uso**

### **Opción 1: Desde Terminal**

```bash
cd "/Users/da_mo/Desktop/6. CONTENT/13. LANDING PAGE"
./update-daily.sh ~/Desktop/photo.jpg ~/Desktop/scan.png "https://youtu.be/VIDEO_ID"
```

### **Opción 2: Desde cualquier lugar**

```bash
/Users/da_mo/Desktop/6.\ CONTENT/13.\ LANDING\ PAGE/update-daily.sh ~/Desktop/photo.jpg ~/Desktop/scan.png "https://youtu.be/VIDEO_ID"
```

---

## 📝 **Parámetros**

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| **photo.jpg** | Ruta a tu foto original | `~/Desktop/photo.jpg` o `/Users/tu_usuario/Desktop/photo.jpg` |
| **scan.png** | Ruta a tu escaneo | `~/Desktop/scan.png` |
| **video_url** | URL completa de YouTube | `https://youtu.be/abc123def456` |

---

## 💡 **Ejemplos reales**

### **Ejemplo 1: Foto en Desktop**
```bash
./update-daily.sh ~/Desktop/photo.jpg ~/Desktop/scan.png "https://youtu.be/abc123"
```

### **Ejemplo 2: Foto en Descargas**
```bash
./update-daily.sh ~/Downloads/photo.jpg ~/Downloads/scan.png "https://youtu.be/xyz789"
```

### **Ejemplo 3: Rutas completas**
```bash
./update-daily.sh /Users/davidmorenogs/Desktop/photo.jpg /Users/davidmorenogs/Desktop/scan.png "https://youtu.be/video123"
```

---

## 🎬 **Cómo obtener el VIDEO_ID de YouTube**

Si tu URL es: `https://www.youtube.com/watch?v=abc123def456`
O links cortos: `https://youtu.be/abc123def456`

El **VIDEO_ID** es: `abc123def456`

Simplemente copia el ID y pasa la URL completa:
```bash
./update-daily.sh photo.jpg scan.png "https://youtu.be/abc123def456"
```

---

## 📁 **Estructura de archivos creada**

Cada día se crea esto automáticamente:

```
/infographics/2026-03-22/
├── photo.jpg
├── scan.png
├── infografico.svg (si lo detecta)
└── manifest.json (actualizado)
```

---

## ✅ **Checklist diario**

Antes de ejecutar:
- [ ] Tienes `photo.jpg` listo
- [ ] Tienes `scan.png` listo
- [ ] Tienes tu video URL de YouTube (`https://youtu.be/VIDEO_ID`)
- [ ] Estás en la carpeta del proyecto o usas ruta completa

---

## 🔍 **Troubleshooting**

### **"❌ Error: Se requieren 3 argumentos"**
→ Asegúrate de pasar exactamente 3 parámetros
```bash
./update-daily.sh photo.jpg scan.png "https://youtu.be/ID"
```

### **"❌ No se encontró foto: photo.jpg"**
→ La ruta a la foto está mal. Usa `~/Desktop/photo.jpg` si está en Desktop

### **"❌ Error en git push"**
→ Asegúrate de que GitHub esté conectado (`git remote -v`)

---

## 📊 **Output esperado**

```
═══════════════════════════════════════════════════════════════
🚀 DELASAC Daily Updater
═══════════════════════════════════════════════════════════════

📅 Fecha: 2026-03-22
📸 Foto: photo.jpg
📄 Scan: scan.png
🎬 Video: https://youtu.be/abc123def456

[1/5] Creando carpeta: ./infographics/2026-03-22
✅ Carpeta creada

[2/5] Copiando archivos...
✅ Foto copiada
✅ Scan copiado

[3/5] Buscando SVG en Desktop...
✅ SVG copiado: infografico.svg

[4/5] Actualizando manifest.json...
✅ Manifest actualizado

[5/5] Publicando a GitHub...
✅ Publicado en GitHub

═══════════════════════════════════════════════════════════════
✅ ¡COMPLETADO! La web se actualizará en ~30 segundos
═══════════════════════════════════════════════════════════════
```

---

## 🚀 **Rutina diaria recomendada**

**Cada día que publiques:**

1. Descarga tu foto original como `photo.jpg`
2. Descarga/prepara tu escaneo como `scan.png`
3. Prepara tu SVG infográfico
4. Ejecuta:
   ```bash
   cd "/Users/da_mo/Desktop/6. CONTENT/13. LANDING PAGE"
   ./update-daily.sh ~/Desktop/photo.jpg ~/Desktop/scan.png "https://youtu.be/VIDEO_ID"
   ```
5. ✅ ¡Listo! Vercel se actualiza automáticamente

---

## 📞 **Soporte**

Si algo falla, verifica:
- ✅ Los archivos existen (prueba `ls ~/Desktop/photo.jpg`)
- ✅ La ruta del script es correcta
- ✅ Git está configurado (`git config user.email`)
- ✅ Tienes conexión a GitHub
