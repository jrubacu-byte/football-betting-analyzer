# 🚀 Guía Completa de Deployment

Esta guía te llevará paso a paso para desplegar tu aplicación de análisis de apuestas deportivas, desde el backend hasta la app móvil.

---

## 📑 Tabla de Contenidos

1. [Resumen General](#resumen-general)
2. [Paso 1: Desplegar Backend en Railway](#paso-1-desplegar-backend-en-railway)
3. [Paso 2: Obtener URL del Backend](#paso-2-obtener-url-del-backend)
4. [Paso 3: Configurar App Móvil](#paso-3-configurar-app-móvil)
5. [Paso 4: Compilar App con EAS](#paso-4-compilar-app-con-eas)
6. [Paso 5: Distribuir la App](#paso-5-distribuir-la-app)
7. [Troubleshooting Común](#troubleshooting-común)
8. [Checklist Final](#checklist-final)

---

## 🎯 Resumen General

### Arquitectura del Sistema

```
┌─────────────────┐
│  App Móvil      │  ← React Native / Expo
│  (Android/iOS)  │
└────────┬────────┘
         │
         │ HTTPS
         │
         ▼
┌─────────────────┐
│  Backend API    │  ← FastAPI / Python
│  (Railway)      │
└────────┬────────┘
         │
         │
         ▼
┌─────────────────┐
│  LLM Service    │  ← Abacus.AI / OpenAI
│  (RouteLLM)     │
└─────────────────┘
```

### Flujo de Deployment

```
1. Backend → Railway       (5-10 min)
2. Obtener URL pública     (1 min)
3. Configurar app móvil    (5 min)
4. Compilar con EAS        (10-20 min)
5. Distribuir APK/IPA      (5 min)
───────────────────────────────────
Total estimado: ~30-45 min
```

---

## 📦 Paso 1: Desplegar Backend en Railway

### 1.1 Preparar el Proyecto

Asegúrate de que todos los archivos de configuración estén en su lugar:

```bash
# Verificar archivos necesarios
ls -la

# Deberías ver:
✓ railway.json
✓ Procfile
✓ runtime.txt
✓ backend/requirements.txt
✓ backend/main.py
✓ backend/config.py
```

### 1.2 Crear Cuenta en Railway

1. Ve a https://railway.app
2. Regístrate con GitHub
3. Autoriza acceso a tus repositorios

### 1.3 Conectar Repositorio

1. Click en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Busca tu repositorio `betting_analysis_app`
4. Railway detectará automáticamente Python

### 1.4 Configurar Variables de Entorno

En el panel de Railway → **Variables**, añade:

```bash
# OBLIGATORIAS
LLM_API_KEY=tu-api-key-aqui
ENVIRONMENT=production

# OPCIONALES (con valores por defecto)
BACKEND_HOST=0.0.0.0
BANKROLL=1000
KELLY_FRACTION=0.25
MIN_EV_THRESHOLD=2.0
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
LOG_LEVEL=INFO
```

⚠️ **IMPORTANTE:** NO configures `PORT`, Railway lo asigna automáticamente.

### 1.5 Deploy

Railway desplegará automáticamente. Monitorea el progreso en la pestaña **"Deployments"**.

```bash
✓ Installing dependencies...
✓ Building application...
✓ Starting uvicorn server...
✓ Deployment live!
```

### 1.6 Verificar Deployment

Ve a la pestaña **"Settings"** → **"Domains"** para ver tu URL.

**📖 Guía detallada:** Ver `RAILWAY_DEPLOYMENT.md`

---

## 🌐 Paso 2: Obtener URL del Backend

### 2.1 Obtener URL Pública

En Railway:
1. Ve a tu proyecto
2. Click en **"Settings"**
3. Sección **"Domains"**
4. Copia la URL (ej: `https://betting-analyzer-production.up.railway.app`)

### 2.2 Probar el Backend

Abre tu navegador y verifica:

**Health Check:**
```
https://TU-URL.up.railway.app/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "environment": "production",
  "version": "1.0.0"
}
```

**API Root:**
```
https://TU-URL.up.railway.app/
```

**Test de Análisis (con Postman/curl):**
```bash
curl -X POST https://TU-URL.up.railway.app/api/analyze \
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

✅ Si obtienes una respuesta JSON con análisis, el backend funciona correctamente.

---

## ⚙️ Paso 3: Configurar App Móvil

### 3.1 Actualizar URL del Backend

Edita `react_native_space/config.js`:

```javascript
const ENV = {
  // ...
  prod: {
    apiUrl: 'https://TU-URL.up.railway.app/api',  // ← CAMBIAR AQUÍ
    environment: 'production',
    logLevel: 'error',
  },
};
```

⚠️ **IMPORTANTE:** Incluye `/api` al final de la URL.

### 3.2 Actualizar CORS en Backend (si es necesario)

Si la app móvil tiene problemas de CORS, añade en Railway → Variables:

```bash
CORS_ORIGINS=https://tu-dominio-frontend.com,exp://localhost:8081
```

### 3.3 Actualizar app.json

Edita `react_native_space/app.json`:

1. **Configurar Project ID:**
   - Ve a https://expo.dev
   - Crea un proyecto nuevo
   - Copia el Project ID
   - Actualiza:

```json
{
  "expo": {
    "extra": {
      "eas": {
        "projectId": "PEGA_TU_PROJECT_ID_AQUI"
      }
    },
    "owner": "tu-username-expo"
  }
}
```

2. **Verificar Bundle IDs (opcional):**

```json
{
  "ios": {
    "bundleIdentifier": "com.bettinganalyzer.app"
  },
  "android": {
    "package": "com.bettinganalyzer.app"
  }
}
```

---

## 📱 Paso 4: Compilar App con EAS

### 4.1 Instalar EAS CLI

```bash
npm install -g eas-cli
```

### 4.2 Login en Expo

```bash
eas login
```

### 4.3 Navegar al Proyecto

```bash
cd react_native_space
```

### 4.4 Compilar para Android (Preview/Testing)

```bash
eas build --platform android --profile preview
```

Este comando:
- ✅ Sube tu código a Expo
- ✅ Compila en la nube (10-20 min)
- ✅ Genera un APK descargable
- ✅ Te da un link de descarga

### 4.5 Compilar para iOS (Opcional)

⚠️ **Requiere Apple Developer Account ($99/año)**

```bash
eas build --platform ios --profile preview
```

### 4.6 Monitorear el Build

Verás algo como:

```bash
✔ Build started
✔ Uploading project...
✔ Building...

Build URL: https://expo.dev/accounts/tu-user/projects/betting-analyzer/builds/xxxxx
```

Abre el URL para ver el progreso en tiempo real.

**📖 Guía detallada:** Ver `EXPO_BUILD.md`

---

## 📤 Paso 5: Distribuir la App

### 5.1 Descargar el APK

Una vez completado el build:

1. Abre el link del build en tu navegador
2. Click en **"Download"**
3. Descarga el archivo `.apk`

### 5.2 Instalar en Android

**Método 1: Instalación directa**
1. Transfiere el APK a tu móvil (USB, email, Drive)
2. Abre el APK en tu móvil
3. Permite "Instalar apps de fuentes desconocidas"
4. Instala

**Método 2: Via ADB**
```bash
adb install nombre-del-archivo.apk
```

**Método 3: Compartir link de Expo**

Expo genera un link público para descargar:
```
https://expo.dev/artifacts/eas/xxxxx.apk
```

Comparte este link con testers.

### 5.3 Distribuir a Testers

**Opciones:**

1. **Google Drive / Dropbox**
   - Sube el APK
   - Comparte el link

2. **Firebase App Distribution**
   - Sube el APK
   - Invita testers por email

3. **TestFlight (iOS)**
   - Sube el IPA a App Store Connect
   - Invita testers

4. **Link directo de Expo**
   - Comparte el link del build

---

## 🐛 Troubleshooting Común

### Backend no responde

**Síntomas:**
- App muestra "Error de conexión"
- Health check falla

**Soluciones:**
1. Verifica que el backend esté activo en Railway
2. Chequea los logs en Railway → Deployments
3. Verifica variables de entorno (especialmente `LLM_API_KEY`)
4. Prueba la URL en navegador

### App no conecta al backend

**Síntomas:**
- App instalada pero no carga datos
- Errores de network

**Soluciones:**
1. Verifica URL en `config.js` (debe incluir `/api`)
2. Asegúrate de compilar después de cambiar la URL
3. Verifica CORS en Railway
4. Prueba la API con Postman

### Build de EAS falla

**Síntomas:**
- Build error en Expo
- "Module not found"

**Soluciones:**
1. Verifica `package.json` para dependencias
2. Ejecuta `npm install` localmente
3. Verifica `app.json` para errores de sintaxis
4. Chequea logs del build en Expo

### APK no instala

**Síntomas:**
- "App no instalada" en Android
- Error de instalación

**Soluciones:**
1. Desinstala versiones anteriores
2. Habilita "Fuentes desconocidas"
3. Verifica espacio disponible
4. Prueba en otro dispositivo

### Variables de entorno no funcionan

**Síntomas:**
- App usa valores incorrectos
- URL del backend no actualizada

**Soluciones:**
1. Verifica `eas.json` → `env` variables
2. Asegúrate de compilar con el perfil correcto
3. Chequea `config.js` lógica de entornos
4. Limpia caché: `eas build --clear-cache`

---

## ✅ Checklist Final

### Backend (Railway)

- [ ] Backend desplegado en Railway
- [ ] Variables de entorno configuradas
- [ ] Health check responde correctamente
- [ ] API endpoint `/api/analyze` funciona
- [ ] CORS configurado para la app móvil
- [ ] Logs verificados sin errores críticos

### App Móvil (Expo EAS)

- [ ] URL del backend actualizada en `config.js`
- [ ] Project ID configurado en `app.json`
- [ ] EAS CLI instalado y login exitoso
- [ ] Build de Android completado
- [ ] APK descargado
- [ ] App instalada y probada en dispositivo
- [ ] Conexión al backend verificada

### Testing

- [ ] Análisis de partidos funciona end-to-end
- [ ] Respuesta del backend se muestra correctamente
- [ ] Historial de análisis guarda correctamente
- [ ] UI responde bien (sin crashes)
- [ ] Probado en al menos 2 dispositivos Android

---

## 📊 Resumen de Costos

| Servicio | Costo | Notas |
|----------|-------|-------|
| Railway (Backend) | $5 gratis/mes | Suficiente para testing |
| Expo EAS Build | 30 builds gratis/mes | Plan gratuito |
| Google Play Console | $25 único | Solo si publicas en Play Store |
| Apple Developer | $99/año | Solo si compilas para iOS |
| **Total (solo Android, testing)** | **$0** | Completamente gratis |
| **Total (con Play Store)** | **$25** | Pago único |
| **Total (con iOS)** | **$124/año** | Incluye Apple Developer |

---

## 🎓 Próximos Pasos

### Mejoras Recomendadas

1. **Analytics:** Integrar Firebase Analytics
2. **Crash Reporting:** Sentry o Bugsnag
3. **Push Notifications:** Expo Notifications
4. **CI/CD:** GitHub Actions para builds automáticos
5. **Testing:** Detox para E2E testing
6. **Monitoring:** Railway alerts + Sentry

### Publicación en Stores

1. **Google Play Store:**
   - Ver: `EXPO_BUILD.md` → Paso 8.1
   - Tiempo de revisión: 1-3 días
   - Costo: $25 (único)

2. **Apple App Store:**
   - Ver: `EXPO_BUILD.md` → Paso 8.2
   - Tiempo de revisión: 1-7 días
   - Costo: $99/año

---

## 📚 Recursos Adicionales

### Documentación Oficial

- 🚂 **Railway Docs:** https://docs.railway.app
- 📱 **Expo Docs:** https://docs.expo.dev
- 🔧 **FastAPI Docs:** https://fastapi.tiangolo.com

### Guías Específicas

- 📖 **Backend Deployment:** `RAILWAY_DEPLOYMENT.md`
- 📖 **Mobile Build:** `EXPO_BUILD.md`
- 📖 **Project README:** `README.md`

### Soporte y Comunidad

- 💬 **Railway Discord:** https://discord.gg/railway
- 💬 **Expo Discord:** https://chat.expo.dev
- 🐛 **GitHub Issues:** Para reportar bugs del proyecto

---

## 🎉 ¡Felicidades!

Has desplegado exitosamente tu aplicación de análisis de apuestas deportivas.

**Tu stack en producción:**
- ✅ Backend FastAPI en Railway
- ✅ App móvil compilada con Expo EAS
- ✅ Sistema completo funcionando end-to-end

**Ahora puedes:**
- 📱 Distribuir la app a usuarios
- 📊 Analizar partidos en tiempo real
- 🚀 Publicar en app stores
- 📈 Escalar según necesidades

---

*Creado para el proyecto de análisis de apuestas deportivas* ⚽️💰🚀
