# RESPONSIVIDAD - Cambios Implementados (21 de Marzo)

## 📱 Breakpoints definidos

| Breakpoint | Rango | Aplicación |
|-----------|-------|------------|
| **Desktop** | ≥1200px | 4 columnas en archivo, lado-a-lado en featured |
| **Desktop M** | 1024px - 1199px | 3 columnas en archivo |
| **Tablet** | 768px - 1023px | 2 columnas en archivo, imágenes apiladas |
| **Mobile L** | 500px - 767px | 2 columnas archivo, scroll vertical |
| **Mobile S** | <500px | Optimizado para phones pequeños |

---

## 🎨 Cambios principales

### 1. **Wrapper (Contenedor principal)**
```css
Antes: max-width: 480px (muy estrecho)
Ahora: max-width: 1400px (full desktop)

Responsive:
- Desktop: 1400px
- Tablet: 100% con padding
- Mobile: 100% con padding menor
```

### 2. **Featured Images (Fotos original + scan)**

**Desktop (≥768px)**:
```
┌─────────────────────────┐
│ Original  │  Scan       │  ← Lado-a-lado
│ (50%)     │  (50%)      │
└─────────────────────────┘
```
- Altura: 400px
- Cada columna: 50% del ancho

**Tablet (768px - 1024px)**:
```
Altura: 350px
Ambas lado-a-lado pero más ajustado
```

**Mobile (≤768px)**:
```
Altura: 500px

┌──────────┐
│ Original │  ← Primera (al entrar)
├──────────┤
│ Scan     │  ← Scroll down
└──────────┘
```

### 3. **Archive Grid (Historial)**

| Breakpoint | Columnas |
|-----------|----------|
| ≥1200px | 4 columnas |
| 1024px | 3 columnas |
| 768px | 2 columnas |
| <768px | 2 columnas (más apretadas) |

Usa `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))` en base.

### 4. **Header responsivo**

**Desktop**: Flex row (logo a un lado, status al otro)
**Mobile**: Stack vertical (logo arriba, status abajo)

**Tamaños de fuente**:
- Desktop: site-name 1.55rem
- Tablet: site-name 1.2rem
- Mobile: site-name 1.1rem

### 5. **Otros elementos**

- **Section labels**: Más pequeños en mobile
- **Footer**: Padding reducido, fuente más pequeña
- **Featured footer**: Flex-wrap para adaptarse
- **All text**: Escala reducida progresivamente

---

## 📏 Comportamiento responsivo

### Entrada en Desktop (1400px)
- Ancho completo: 1400px máximo
- Featured: 1400px × 400px (lado-a-lado)
- Archive: 4 columnas en grid
- Padding lateral: 1.25rem

### Redimensionar a Tablet (1024px)
- Archive pasa a 3 columnas
- Featured sigue lado-a-lado
- Padding: 1.25rem

### Redimensionar a Mobile (600px)
- Featured apila: Original arriba, Scan abajo
- Archive a 2 columnas
- Header apila: Logo arriba, Status abajo
- Padding: 0.75rem

### En Mobile pequeño (<500px)
- Todo igual pero con espacios menores
- Fuentes más pequeñas (~10-15% menos)
- Padding: 0.75rem

---

## 🔍 Testing responsividad

Abre DevTools (F12) y prueba:

**Desktop**:
- Ancho: 1400px
- Expected: Original | Scan lado-a-lado
- Archive: 4 columnas

**Tablet**:
- Ancho: 1024px
- Expected: Original | Scan lado-a-lado
- Archive: 3 columnas

**Mobile**:
- Ancho: 768px
- Expected: Original arriba
- Luego scroll: Scan abajo
- Archive: 2 columnas

**Mobile pequeño**:
- Ancho: 375px
- Expected: Todo apilado
- Fuentes pequeñas

---

## ✨ Ventajas implementadas

✅ **Full-width en desktop** (aprovecha mejor espacio)
✅ **Mobile-first en small phones** (scroll natural)
✅ **Transiciones suaves** entre breakpoints
✅ **Sin saltos visuales** (media queries bien calibradas)
✅ **Touch-friendly** en móvil (tamaños adequados)
✅ **Performance** (media queries optimizadas)

---

## 🚀 Próxima prueba

Prueba en navegador real con:
- iPhone 12 / 13 / 14 (390px - 430px)
- iPad (768px - 1024px)
- Desktop (1400px+)

Verifica que:
1. Desktop: Original y Scan lado-a-lado ✓
2. Mobile: Scroll vertical natural ✓
3. Sin espacios en blanco inadecuados ✓
4. Texto legible en todos los tamaños ✓
