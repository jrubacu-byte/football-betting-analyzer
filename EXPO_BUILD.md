# 📱 Guía de Compilación con Expo EAS Build

Esta guía te ayudará a compilar tu app móvil de análisis de apuestas usando **Expo EAS Build** (Expo Application Services), generando archivos APK/AAB para Android e IPA para iOS.

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener:

1. ✅ **Node.js 18+** instalado
2. ✅ **Cuenta de Expo** (gratis en https://expo.dev)
3. ✅ **Backend desplegado en Railway** con URL pública
4. ✅ **Git** instalado y repositorio sincronizado
5. ✅ (Opcional) **Cuenta de desarrollador Apple** para iOS ($99/año)

---

## 🚀 Paso 1: Instalar EAS CLI

### 1.1 Instalar Globalmente

```bash
npm install -g eas-cli
```

### 1.2 Verificar Instalación

```bash
eas --version
# Debería mostrar: eas-cli/5.x.x
```

### 1.3 Login en Expo

```bash
eas login
```

Introduce tus credenciales de Expo o crea una cuenta nueva.

---

## ⚙️ Paso 2: Configurar el Proyecto

### 2.1 Navegar al Directorio

```bash
cd react_native_space
```

### 2.2 Configurar EAS Build

```bash
eas build:configure
```

Este comando:
- Detectará tu `app.json`
- Creará `eas.json` (ya lo tenemos configurado)
- Te pedirá confirmación

### 2.3 Actualizar URLs del Backend

Edita `config.js` con la URL de tu backend en Railway:

```javascript
const ENV = {
  // ...
  prod: {
    apiUrl: 'https://TU-PROYECTO.up.railway.app/api',  // ← CAMBIAR ESTO
    environment: 'production',
    logLevel: 'error',
  },
};
```

### 2.4 Actualizar app.json

Edita `app.json` para configurar:

1. **Project ID de Expo:**
   - Ve a https://expo.dev
   - Crea un nuevo proyecto o selecciona uno existente
   - Copia el Project ID
   - Actualiza en `app.json`:

```json
{
  "expo": {
    "extra": {
      "eas": {
        "projectId": "TU_PROJECT_ID_AQUI"
      }
    },
    "owner": "tu-username-expo"
  }
}
```

2. **Bundle Identifiers (si quieres cambiarlos):**

```json
{
  "ios": {
    "bundleIdentifier": "com.tuempresa.bettinganalyzer"
  },
  "android": {
    "package": "com.tuempresa.bettinganalyzer"
  }
}
```

---

## 📦 Paso 3: Compilar para Android

### 3.1 Build de Preview (APK para Testing)

Este es el build más común para testing:

```bash
eas build --platform android --profile preview
```

**Ventajas:**
- ✅ Genera un archivo **APK** directo
- ✅ Fácil de instalar en cualquier Android
- ✅ No requiere Google Play Store
- ✅ Ideal para testers y demo

**Proceso:**
1. EAS subirá tu código a los servidores de Expo
2. Compilará la app en la nube (5-15 minutos)
3. Te dará un link para descargar el APK

### 3.2 Build de Producción (AAB para Play Store)

Para publicar en Google Play Store:

```bash
eas build --platform android --profile production
```

**Genera:**
- ✅ **AAB** (Android App Bundle)
- ✅ Optimizado para Play Store
- ✅ Tamaño reducido

### 3.3 Build de Development

Para desarrollo con hot reload:

```bash
eas build --platform android --profile development
```

**Nota:** Requiere Expo Go o Development Build.

---

## 🍎 Paso 4: Compilar para iOS

### 4.1 Requisitos para iOS

**IMPORTANTE:** Para compilar iOS necesitas:

1. **Cuenta de Apple Developer** ($99/año)
2. **Certificados y provisioning profiles** (EAS los maneja automáticamente)

### 4.2 Build de Preview (para Testing)

```bash
eas build --platform ios --profile preview
```

**Opciones de distribución:**
- **Ad Hoc:** Hasta 100 dispositivos registrados
- **TestFlight:** Testing con usuarios externos

### 4.3 Build de Producción

```bash
eas build --platform ios --profile production
```

Genera un archivo **IPA** listo para App Store.

### 4.4 Registro de Dispositivos

Para testing en dispositivos específicos:

```bash
eas device:create
```

---

## 🌍 Paso 5: Build Multiplataforma

Para compilar Android e iOS al mismo tiempo:

```bash
eas build --platform all --profile preview
```

**Nota:** iOS fallará si no tienes cuenta de Apple Developer.

---

## 📥 Paso 6: Descargar y Distribuir

### 6.1 Monitorear el Build

Durante el build, verás:

```bash
✔ Build started
✔ Uploading project...
✔ Building...
✔ Build finished

Build URL: https://expo.dev/accounts/tu-username/projects/betting-analyzer/builds/xxxxx
```

### 6.2 Descargar el APK/IPA

**Opción 1: Desde la Web**
1. Abre el link del build
2. Haz clic en "Download"
3. Descarga el archivo APK o IPA

**Opción 2: Desde CLI**

```bash
eas build:list
```

Esto mostrará todos tus builds con links de descarga.

### 6.3 Instalar en Android

**Método 1: Via Link**
1. Abre el link del build en tu móvil Android
2. Descarga el APK
3. Permitir "Instalar apps de fuentes desconocidas"
4. Instalar el APK

**Método 2: Via ADB**

```bash
# Conectar dispositivo via USB
adb devices

# Instalar APK
adb install nombre-del-archivo.apk
```

**Método 3: Google Drive / Dropbox**
1. Sube el APK a Drive/Dropbox
2. Comparte el link con testers
3. Descargan e instalan

### 6.4 Instalar en iOS

**Método 1: TestFlight (Recomendado)**
1. Sube el IPA a App Store Connect
2. Invita testers via email
3. Ellos instalan desde TestFlight app

**Método 2: Ad Hoc**
1. Registra UDIDs de dispositivos
2. Genera build ad hoc
3. Distribuye via link directo

---

## 🔄 Paso 7: Actualizar la App

### 7.1 Incrementar Versión

Edita `app.json`:

```json
{
  "expo": {
    "version": "1.0.1",  // ← Incrementar
    "android": {
      "versionCode": 2   // ← Incrementar (Android)
    },
    "ios": {
      "buildNumber": "2" // ← Incrementar (iOS)
    }
  }
}
```

### 7.2 Compilar Nueva Versión

```bash
eas build --platform android --profile preview
```

### 7.3 OTA Updates (Over-The-Air)

Para actualizaciones sin recompilar:

```bash
eas update --branch production --message "Bug fixes"
```

**Ventajas:**
- ✅ Actualización instantánea
- ✅ Sin necesidad de recompilar
- ✅ Sin pasar por app stores
- ✅ Solo para código JavaScript (no para código nativo)

---

## 📤 Paso 8: Publicar en Stores

### 8.1 Google Play Store

#### Preparar

1. Crea una cuenta de Google Play Console ($25 único)
2. Crea una nueva aplicación
3. Completa información (nombre, descripción, screenshots)

#### Subir AAB

```bash
# Generar AAB de producción
eas build --platform android --profile production

# Subir a Play Store
eas submit --platform android
```

#### Configurar en Play Console

1. Sube el AAB descargado
2. Configura precios y distribución
3. Completa cuestionario de contenido
4. Enviar para revisión (1-3 días)

### 8.2 Apple App Store

#### Preparar

1. Cuenta de Apple Developer ($99/año)
2. Crear App ID en developer.apple.com
3. Configurar App Store Connect

#### Subir IPA

```bash
# Generar IPA de producción
eas build --platform ios --profile production

# Subir a App Store
eas submit --platform ios
```

#### Configurar en App Store Connect

1. Completa información de la app
2. Añade screenshots y preview videos
3. Configura precios
4. Enviar para revisión (1-7 días)

---

## 🔍 Paso 9: Testing y QA

### 9.1 Testing Interno

**Android:**
```bash
eas build --platform android --profile preview
```

Distribuye el APK a tu equipo vía:
- Google Drive
- Dropbox
- TestFlight (Android)
- Firebase App Distribution

**iOS:**
```bash
eas build --platform ios --profile preview
```

Distribuye via TestFlight:
1. Sube el build a App Store Connect
2. Invita testers internos (hasta 100)
3. Ellos reciben notificación en TestFlight app

### 9.2 Testing con Usuarios Externos

**TestFlight (iOS):**
- Hasta 10,000 testers externos
- Requiere revisión de Apple (1-2 días)

**Google Play Beta:**
- Testing cerrado o abierto
- Distribución via Play Store

---

## 🐛 Troubleshooting

### Problema 1: "Build failed: Missing credentials"

**Causa:** EAS no tiene certificados de firma

**Solución:**

```bash
# Android
eas credentials

# iOS
eas credentials --platform ios
```

EAS generará certificados automáticamente.

### Problema 2: "Module not found: expo-constants"

**Causa:** Dependencia faltante

**Solución:**

```bash
cd react_native_space
npm install expo-constants
```

### Problema 3: "API_ENV not defined"

**Causa:** Variable de entorno no configurada en `eas.json`

**Solución:**

Verifica `eas.json`:

```json
{
  "build": {
    "preview": {
      "env": {
        "API_ENV": "staging"
      }
    }
  }
}
```

### Problema 4: "App no conecta al backend"

**Causa:** URL incorrecta en `config.js`

**Solución:**

1. Verifica URL de Railway
2. Asegúrate de que incluya `/api`
3. Verifica CORS en el backend
4. Prueba la URL en navegador

```javascript
// Correcto
apiUrl: 'https://tu-proyecto.up.railway.app/api'

// Incorrecto
apiUrl: 'https://tu-proyecto.up.railway.app'  // Sin /api
```

### Problema 5: "Build timeout"

**Causa:** Build muy lento o recursos insuficientes

**Solución:**

- Espera y reintenta
- Verifica `package.json` para dependencias pesadas
- Usa `.easignore` para excluir archivos innecesarios

### Problema 6: "Invalid bundle identifier"

**Causa:** Bundle ID ya en uso o formato incorrecto

**Solución:**

```json
{
  "ios": {
    "bundleIdentifier": "com.TUEMPRESA.TUAPP"  // Único y válido
  },
  "android": {
    "package": "com.tuempresa.tuapp"  // Minúsculas
  }
}
```

---

## 💡 Mejores Prácticas

### 1. Versionado

**Semantic Versioning:**
- `1.0.0` → Primera versión
- `1.0.1` → Bug fixes
- `1.1.0` → Nuevas features
- `2.0.0` → Breaking changes

### 2. Testing

- ✅ Prueba en preview antes de production
- ✅ Test en múltiples dispositivos Android
- ✅ Verifica integración con backend
- ✅ Prueba offline mode (si aplica)

### 3. Distribución

- ✅ Usa TestFlight para iOS beta testing
- ✅ Google Play Beta para Android testing
- ✅ Recolecta feedback de usuarios
- ✅ Itera antes de lanzar a producción

### 4. Seguridad

- ✅ Nunca commitees secrets al repositorio
- ✅ Usa variables de entorno para API keys
- ✅ Configura CORS correctamente en backend
- ✅ Usa HTTPS siempre

### 5. Optimización

- ✅ Minimiza tamaño del bundle
- ✅ Usa lazy loading cuando sea posible
- ✅ Optimiza imágenes
- ✅ Reduce dependencias innecesarias

---

## 📊 Costos

### Expo EAS Build

**Plan Gratuito:**
- ✅ 30 builds/mes
- ✅ Perfecto para testing y desarrollo
- ✅ Sin tarjeta de crédito requerida

**Plan Paid:**
- **$29/mes:** 500 builds/mes
- **$99/mes:** 2000 builds/mes

### App Stores

- **Google Play Console:** $25 (pago único)
- **Apple Developer Program:** $99/año

### Total Estimado

- **Solo Android:** ~$25 (único)
- **Solo iOS:** ~$99/año
- **Ambos:** ~$124 primer año, $99/año después

---

## 📚 Recursos Adicionales

- 📖 **EAS Build Docs:** https://docs.expo.dev/build/introduction/
- 💬 **Expo Discord:** https://chat.expo.dev
- 🎓 **Expo YouTube:** Tutoriales de builds
- 🐛 **Expo Forums:** https://forums.expo.dev

---

## ✨ Próximos Pasos

Una vez que tengas tu app compilada:

1. ✅ Prueba en dispositivos reales
2. ✅ Recolecta feedback de usuarios
3. ✅ Itera y mejora
4. ✅ Publica en stores
5. ✅ Configura analytics y crash reporting

---

## 🎉 ¡Felicidades!

Tu app móvil está compilada y lista para distribución. Ahora puedes:

- 📱 Instalarla en cualquier Android
- 🍎 Distribuirla via TestFlight (iOS)
- 🚀 Publicarla en Google Play / App Store
- 🔄 Actualizarla con OTA updates

---

*Creado para el proyecto de análisis de apuestas deportivas* ⚽️💰📱
