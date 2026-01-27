# ⚽ Football Betting Analyzer

Sistema profesional de análisis de apuestas deportivas con Expected Value (EV+) y gestión de riesgo.

## 🎯 Características

- **Análisis Inteligente**: LLM + Modelos Matemáticos (Poisson, Binomial)
- **Cálculo de EV**: Identifica oportunidades con valor positivo
- **Gestión de Riesgo**: Kelly Criterion para stake óptimo
- **Interfaz Móvil**: React Native con Expo
- **Backend Robusto**: FastAPI con análisis en tiempo real
- **Historial**: Almacenamiento local de análisis

## 📋 Requisitos

### Backend
- Python 3.11+
- pip
- Docker (opcional)

### Mobile
- Node.js 16+
- npm o yarn
- Expo CLI
- iOS/Android emulator o dispositivo físico

## 🚀 Instalación

### 1. Backend

```bash
# Clonar repositorio
git clone <repo-url>
cd football-betting-analyzer

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r backend/requirements.txt

# Configurar variables de entorno
cp backend/.env.example backend/.env
# Editar backend/.env con tu LLM_API_KEY

# Iniciar servidor
python -m backend.main
```

El backend estará disponible en `http://localhost:8000`

### 2. Mobile App

```bash
# Navegar a carpeta mobile
cd react_native_space

# Instalar dependencias
npm install

# Configurar API URL
cp .env.example .env
# Editar .env con tu API_URL (ej: http://192.168.1.100:8000/api)

# Iniciar Expo
expo start

# En otra terminal:
# Para iOS: expo start --ios
# Para Android: expo start --android
# Para Web: expo start --web
```

## 🐳 Despliegue con Docker

```bash
# Crear archivo .env
cp backend/.env.example backend/.env
# Editar con tus valores

# Iniciar con docker-compose
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Detener
docker-compose down
```

## 📱 Uso de la App

### Pantalla 1: Análisis
1. Introduce el nombre del partido (ej: "Ajax vs Olympiacos")
2. Introduce las cuotas 1X2 de tu bookmaker
3. (Opcional) Introduce cuotas adicionales (goles, tarjetas, etc.)
4. Toca "Analizar Partido"
5. Espera el análisis (10-15 segundos)

### Pantalla 2: Resultados
- **Apuesta Recomendada**: Selección con mejor EV
- **Gráfico de Probabilidades**: Distribución 1X2
- **Análisis de Mercados**: Comparativa cuotas justas vs bookie
- **Datos Clave**: Insights del análisis
- **Otras Oportunidades**: Alternativas con EV+

### Pantalla 3: Historial
- Visualiza todos tus análisis guardados
- Fecha y hora de cada análisis
- Recomendación y EV de cada uno

## 🔌 API Endpoints

### Health Check
```
GET /health
```

### Análisis de Partido
```
POST /api/analyze

Body:
{
  "match_name": "Ajax vs Olympiacos",
  "odds": {
    "home_win": 1.50,
    "draw": 3.50,
    "away_win": 6.00,
    "over_2_5": 1.80,
    "btts_yes": 1.95
  },
  "bankroll": 1000
}

Response:
{
  "match_name": "Ajax vs Olympiacos",
  "prob_home_win": 0.65,
  "prob_draw": 0.20,
  "prob_away_win": 0.15,
  "top_recommendation": {
    "selection": "Victoria Local",
    "odds": 1.50,
    "ev_percent": 8.5,
    "stake_suggested": 25.50
  },
  "key_insights": [...]
}
```

## 🧪 Testing

### Backend
```bash
# Instalar pytest
pip install pytest pytest-asyncio

# Ejecutar tests
pytest backend/tests/
```

### Mobile
```bash
# Instalar jest
npm install --save-dev jest

# Ejecutar tests
npm test
```

## 🚀 Deployment en Producción

### Railway (Backend)

Despliega el backend en Railway para tenerlo disponible 24/7:

```bash
# 1. Crea cuenta en https://railway.app
# 2. Conecta tu repositorio de GitHub
# 3. Configura variables de entorno en Railway
# 4. Deploy automático

# Variables requeridas:
LLM_API_KEY=tu-api-key
ENVIRONMENT=production
```

**Guía completa:** Ver `RAILWAY_DEPLOYMENT.md`

### Expo EAS Build (Mobile)

Compila la app móvil para distribución:

```bash
# Instalar EAS CLI
npm install -g eas-cli

# Login en Expo
eas login

# Compilar para Android
cd react_native_space
eas build --platform android --profile preview

# Compilar para iOS (requiere Apple Developer Account)
eas build --platform ios --profile preview
```

**Guía completa:** Ver `EXPO_BUILD.md`

### Guía de Deployment Completa

Para un walkthrough paso a paso de todo el proceso:

📖 **Ver:** `DEPLOYMENT_GUIDE.md`

**Incluye:**
- ✅ Deployment de backend en Railway
- ✅ Configuración de variables de entorno
- ✅ Compilación de app móvil con EAS
- ✅ Distribución de APK/IPA
- ✅ Troubleshooting común
- ✅ Checklist de verificación

**Tiempo estimado:** 30-45 minutos

## 📊 Arquitectura

```
┌─────────────────────────────────────────┐
│         Mobile App (React Native)       │
│  ┌─────────────────────────────────┐   │
│  │  Input Screen → Analysis Screen │   │
│  │  ↓                              │   │
│  │  AsyncStorage (Historial)       │   │
│  └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │ HTTP/REST
               ↓
┌─────────────────────────────────────────┐
│      Backend (FastAPI + Python)         │
│  ┌─────────────────────────────────┐   │
│  │  LLM Client (Web Search)        │   │
│  │  ↓                              │   │
│  │  Analysis Engine (Poisson)      │   │
│  │  ↓                              │   │
│  │  Betting Engine (Kelly)         │   │
│  │  ↓                              │   │
│  │  Response Formatter             │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## 🔐 Seguridad

- Variables de entorno para credenciales
- CORS configurado
- Validación de entrada con Pydantic
- Logging de todas las operaciones
- Timeout en requests

## 📈 Roadmap

- [ ] Base de datos para historial persistente
- [ ] Autenticación de usuarios
- [ ] Dashboard web
- [ ] Notificaciones push
- [ ] Integración con APIs de bookmakers
- [ ] Machine Learning para mejora de predicciones
- [ ] Backtesting automático

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT.

## 📞 Soporte

Para reportar bugs o sugerencias, abre un issue en GitHub.
