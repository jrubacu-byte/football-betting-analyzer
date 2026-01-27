# 🚂 Guía de Deployment en Railway

Esta guía te ayudará a desplegar el backend FastAPI de tu aplicación de análisis de apuestas en **Railway**, un servicio de hosting moderno y fácil de usar.

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener:

1. ✅ Cuenta de GitHub con el repositorio del proyecto
2. ✅ Cuenta de Railway (gratis en https://railway.app)
3. ✅ API Key de tu servicio LLM (para análisis)

---

## 🚀 Paso 1: Crear Cuenta en Railway

### 1.1 Registro

1. Ve a https://railway.app
2. Haz clic en **"Start a New Project"** o **"Login"**
3. Registrate con tu cuenta de **GitHub** (recomendado)
4. Autoriza a Railway para acceder a tus repositorios

### 1.2 Verificar Cuenta

Railway ofrece un plan gratuito con límites generosos:
- **$5 USD de crédito gratis por mes**
- Sin necesidad de tarjeta de crédito inicialmente
- Perfecto para proyectos pequeños y testing

---

## 🔗 Paso 2: Conectar Repositorio de GitHub

### 2.1 Crear Nuevo Proyecto

1. En el dashboard de Railway, haz clic en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Busca y selecciona tu repositorio `betting_analysis_app`
4. Railway detectará automáticamente que es un proyecto Python

### 2.2 Configuración Automática

Railway detectará:
- ✅ `runtime.txt` → Python 3.11
- ✅ `requirements.txt` → Instalará dependencias
- ✅ `Procfile` o `railway.json` → Comando de inicio
- ✅ `/health` endpoint → Health check

---

## ⚙️ Paso 3: Configurar Variables de Entorno

### 3.1 Variables Obligatorias

En el panel de Railway, ve a **"Variables"** y añade:

```bash
# LLM Configuration (OBLIGATORIO)
LLM_API_KEY=tu-api-key-aqui

# Environment
ENVIRONMENT=production

# Backend Configuration (Railway asigna PORT automáticamente)
BACKEND_HOST=0.0.0.0

# Betting Configuration
BANKROLL=1000
KELLY_FRACTION=0.25
MIN_EV_THRESHOLD=2.0
```

### 3.2 Variables Opcionales

```bash
# LLM Settings
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7

# CORS Origins (añade tu dominio frontend cuando esté listo)
CORS_ORIGINS=https://tu-app-frontend.com

# Logging
LOG_LEVEL=INFO

# Custom Domain (si tienes uno)
CUSTOM_DOMAIN=api.tudominio.com
```

### 3.3 Cómo Añadir Variables

1. En tu proyecto de Railway, selecciona tu servicio
2. Ve a la pestaña **"Variables"**
3. Haz clic en **"New Variable"**
4. Añade nombre y valor
5. Haz clic en **"Add"**

**⚠️ IMPORTANTE:** Railway asigna automáticamente la variable `PORT`. **NO** la configures manualmente.

---

## 🎯 Paso 4: Desplegar

### 4.1 Deploy Automático

1. Railway desplegará automáticamente al crear el proyecto
2. Puedes ver el progreso en la pestaña **"Deployments"**
3. El primer deployment puede tardar 2-5 minutos

### 4.2 Monitorear el Build

```bash
# Verás logs como:
Installing dependencies from requirements.txt
Building application...
Starting uvicorn server...
✓ Deployment live!
```

### 4.3 Obtener URL Pública

Una vez desplegado:

1. Ve a la pestaña **"Settings"**
2. Busca la sección **"Domains"**
3. Verás algo como: `https://tu-proyecto-production.up.railway.app`
4. Railway también puede generar una URL más corta

### 4.4 Añadir Dominio Personalizado (Opcional)

Si tienes un dominio propio:

1. Ve a **Settings → Domains**
2. Haz clic en **"Add Domain"**
3. Ingresa tu dominio (ej: `api.tudominio.com`)
4. Configura el DNS según las instrucciones de Railway
5. Railway generará certificado SSL automáticamente

---

## ✅ Paso 5: Verificar Deployment

### 5.1 Probar Health Check

Abre tu navegador y ve a:

```
https://tu-proyecto.up.railway.app/health
```

Deberías ver:

```json
{
  "status": "healthy",
  "environment": "production",
  "version": "1.0.0"
}
```

### 5.2 Probar API Root

```
https://tu-proyecto.up.railway.app/
```

Respuesta esperada:

```json
{
  "message": "Football Betting Analyzer API",
  "docs": "/docs",
  "health": "/health"
}
```

### 5.3 Probar Endpoint de Análisis

Usa Postman, curl o cualquier cliente HTTP:

```bash
curl -X POST https://tu-proyecto.up.railway.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "match_name": "Real Madrid vs Barcelona",
    "odds": {
      "home_win": 2.10,
      "draw": 3.40,
      "away_win": 3.50
    },
    "bankroll": 1000
  }'
```

---

## 📊 Paso 6: Ver Logs y Monitoreo

### 6.1 Ver Logs en Tiempo Real

1. En tu proyecto de Railway, ve a la pestaña **"Deployments"**
2. Haz clic en el deployment activo
3. Verás los logs en tiempo real
4. Busca errores o advertencias

### 6.2 Logs Importantes

```bash
# Inicio exitoso
INFO: Started server process
INFO: Uvicorn running on 0.0.0.0:XXXX

# Requests entrantes
INFO: POST /api/analyze - 200 OK

# Errores
ERROR: Missing LLM_API_KEY
WARNING: High response time detected
```

### 6.3 Métricas

Railway proporciona métricas automáticas:
- **CPU Usage** - Uso de procesador
- **Memory Usage** - Uso de memoria
- **Network** - Tráfico de red
- **Response Times** - Tiempos de respuesta

---

## 🔄 Paso 7: Actualizaciones y Re-deploys

### 7.1 Deploy Automático

Railway re-despliega automáticamente cuando:
- Haces `git push` a la rama principal
- Cambias variables de entorno
- Modificas la configuración del proyecto

### 7.2 Deploy Manual

1. Ve a **Deployments**
2. Haz clic en **"Redeploy"** en el último deployment
3. Confirma la acción

### 7.3 Rollback

Si algo sale mal:

1. Ve a **Deployments**
2. Busca un deployment anterior exitoso
3. Haz clic en **"Redeploy"**
4. Railway restaurará esa versión

---

## 🐛 Troubleshooting

### Problema 1: "Application failed to respond"

**Causa:** El servidor no está respondiendo en el puerto correcto

**Solución:**
- Verifica que uses `PORT` de variable de entorno (no hardcodeado)
- Chequea `railway.json` y `Procfile`
- Verifica logs para errores de inicio

```python
# En config.py (ya está configurado)
BACKEND_PORT = int(os.getenv("PORT", os.getenv("BACKEND_PORT", "8000")))
```

### Problema 2: "Module not found"

**Causa:** Dependencias no instaladas correctamente

**Solución:**
- Verifica que `requirements.txt` esté en la raíz
- Asegúrate de que todas las dependencias estén listadas
- Re-deploya el proyecto

### Problema 3: "LLM_API_KEY not found"

**Causa:** Variable de entorno no configurada

**Solución:**
- Ve a **Variables** en Railway
- Añade `LLM_API_KEY` con tu API key
- El proyecto se re-desplegará automáticamente

### Problema 4: "CORS error"

**Causa:** El frontend no está en CORS_ORIGINS

**Solución:**
- Añade la URL de tu app móvil/frontend a `CORS_ORIGINS`
- Ejemplo: `CORS_ORIGINS=https://tu-app-frontend.com,https://expo.dev/@tu-usuario/tu-app`

### Problema 5: "503 Service Unavailable"

**Causa:** La aplicación está caída o en proceso de deployment

**Solución:**
- Espera unos minutos (deployment en progreso)
- Verifica logs para errores críticos
- Revisa el uso de recursos (CPU/Memory)

### Problema 6: Build muy lento

**Causa:** Dependencias pesadas (numpy, scipy)

**Solución:**
- Railway cachea dependencias después del primer build
- Los siguientes builds serán mucho más rápidos
- Primer build: ~3-5 minutos
- Builds siguientes: ~1-2 minutos

---

## 💰 Gestión de Costos

### Plan Gratuito

Railway ofrece:
- **$5 USD de crédito gratis por mes**
- Suficiente para ~500,000 requests/mes en apps pequeñas
- Sin tarjeta de crédito requerida

### Optimizar Uso

1. **Reducir idle time:** Railway cobra por tiempo de ejecución
2. **Usar sleep mode:** Configurar inactividad después de 30 min
3. **Monitorear métricas:** Revisar uso de CPU/memoria
4. **Optimizar código:** Reducir tiempo de respuesta

### Costos Típicos

Para una app de análisis de apuestas:
- **Desarrollo/Testing:** Gratis ($5 de crédito mensual)
- **Producción baja:** $1-3 USD/mes
- **Producción media:** $5-10 USD/mes

---

## 🔒 Seguridad

### Mejores Prácticas

1. ✅ **Nunca** commitees API keys al repositorio
2. ✅ Usa variables de entorno para secretos
3. ✅ Configura CORS correctamente
4. ✅ Usa HTTPS (Railway lo hace automáticamente)
5. ✅ Limita hosts con `TrustedHostMiddleware`
6. ✅ Monitorea logs regularmente

---

## 📚 Recursos Adicionales

- 📖 **Railway Docs:** https://docs.railway.app
- 💬 **Railway Discord:** https://discord.gg/railway
- 🎓 **Railway Blog:** https://blog.railway.app
- 🐛 **GitHub Issues:** Para reportar bugs

---

## ✨ Próximos Pasos

Una vez que tu backend esté desplegado:

1. ✅ Guarda la URL pública de Railway
2. ✅ Actualiza `react_native_space/config.js` con la URL
3. ✅ Compila la app móvil con Expo EAS Build
4. ✅ Prueba la integración completa

Ver: `EXPO_BUILD.md` para compilar la app móvil

---

## 🎉 ¡Felicidades!

Tu backend ahora está desplegado en Railway y listo para recibir requests desde tu app móvil.

**URL de tu API:** `https://tu-proyecto.up.railway.app`

---

*Creado para el proyecto de análisis de apuestas deportivas* ⚽️💰
