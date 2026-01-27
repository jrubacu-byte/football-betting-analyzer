# 🛠️ Scripts de Utilidad

Esta carpeta contiene scripts de shell para automatizar tareas comunes de desarrollo y deployment.

---

## 📜 Scripts Disponibles

### 1. `test_backend.sh`

Prueba el backend localmente antes de desplegar.

**Uso:**
```bash
./scripts/test_backend.sh
```

**Qué hace:**
- ✅ Verifica instalación de Python 3.11+
- ✅ Crea/activa virtual environment
- ✅ Instala dependencias
- ✅ Verifica variables de entorno
- ✅ Ejecuta tests unitarios con pytest
- ✅ Inicia servidor temporalmente
- ✅ Prueba endpoints de health y root
- ✅ Detiene servidor automáticamente

**Cuándo usar:**
- Antes de hacer commit
- Antes de desplegar en Railway
- Después de cambios en el código
- Para verificar configuración local

---

### 2. `deploy_railway.sh`

Automatiza el deployment del backend en Railway.

**Uso:**
```bash
./scripts/deploy_railway.sh
```

**Qué hace:**
- ✅ Verifica Railway CLI instalado
- ✅ Verifica autenticación
- ✅ Ejecuta tests del backend
- ✅ Verifica archivos de configuración
- ✅ Vincula con proyecto Railway
- ✅ Muestra variables de entorno
- ✅ Despliega a Railway
- ✅ Muestra URL del deployment

**Requisitos previos:**
- Railway CLI instalado (el script lo instala si no existe)
- Cuenta de Railway
- Repositorio Git configurado
- `railway.json` en la raíz del proyecto

**Cuándo usar:**
- Para desplegar cambios a producción
- Después de actualizar el backend
- Para crear nuevo deployment

---

### 3. `build_mobile.sh`

Compila la app móvil con Expo EAS Build.

**Uso:**
```bash
# Compilar para Android
./scripts/build_mobile.sh android

# Compilar para iOS
./scripts/build_mobile.sh ios

# Compilar para ambos
./scripts/build_mobile.sh all
```

**Qué hace:**
- ✅ Verifica EAS CLI instalado
- ✅ Verifica autenticación de Expo
- ✅ Verifica configuración de app.json
- ✅ Valida URL del backend
- ✅ Permite elegir perfil (preview/production/development)
- ✅ Inicia build en la nube
- ✅ Muestra link de descarga
- ✅ Lista últimos builds

**Perfiles disponibles:**
- **preview**: APK/Ad Hoc para testing
- **production**: AAB/IPA para app stores
- **development**: Build de desarrollo con hot reload

**Requisitos previos:**
- EAS CLI instalado (el script lo instala si no existe)
- Cuenta de Expo
- Project ID configurado en app.json
- Apple Developer Account (solo para iOS)

**Cuándo usar:**
- Para generar builds de testing
- Para preparar versión de producción
- Después de cambios en la app móvil

---

## 🚀 Flujo de Trabajo Recomendado

### Desarrollo Local

```bash
# 1. Hacer cambios en el código
# 2. Probar localmente
./scripts/test_backend.sh

# 3. Si pasan los tests, hacer commit
git add .
git commit -m "Descripción de cambios"
git push
```

### Deployment a Producción

```bash
# 1. Desplegar backend
./scripts/deploy_railway.sh

# 2. Obtener URL del backend
# (El script la muestra al final)

# 3. Actualizar config.js con la URL

# 4. Compilar app móvil
./scripts/build_mobile.sh android

# 5. Descargar APK y distribuir
```

---

## 🔧 Solución de Problemas

### Script no ejecutable

```bash
chmod +x scripts/*.sh
```

### Railway CLI no funciona

```bash
npm install -g @railway/cli
railway login
```

### EAS CLI no funciona

```bash
npm install -g eas-cli
eas login
```

### Tests fallan

```bash
# Verifica variables de entorno
cat backend/.env

# Reinstala dependencias
pip install -r backend/requirements.txt

# Ejecuta tests manualmente
pytest backend/ -v
```

### Build de mobile falla

```bash
# Verifica configuración
cat react_native_space/app.json

# Limpia caché
cd react_native_space
eas build --clear-cache
```

---

## 📚 Recursos Adicionales

- **Railway Docs:** https://docs.railway.app
- **EAS Build Docs:** https://docs.expo.dev/build/introduction/
- **Testing con pytest:** https://docs.pytest.org/

---

## 💡 Tips

1. **Ejecuta `test_backend.sh` siempre antes de desplegar**
2. **Usa profile "preview" para testing de mobile**
3. **Verifica la URL del backend antes de compilar mobile**
4. **Guarda los links de descarga de los builds de EAS**
5. **Haz commit de cambios antes de desplegar**

---

*Scripts creados para el proyecto de análisis de apuestas deportivas* ⚽️💰
