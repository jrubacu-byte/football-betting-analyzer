import os
from dotenv import load_dotenv

load_dotenv()

# Backend Configuration
BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
# Railway asigna el puerto dinámicamente mediante la variable PORT
BACKEND_PORT = int(os.getenv("PORT", os.getenv("BACKEND_PORT", "8000")))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# LLM Configuration
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.7))

# Betting Configuration
BANKROLL = float(os.getenv("BANKROLL", 1000))
KELLY_FRACTION = float(os.getenv("KELLY_FRACTION", 0.25))
MIN_EV_THRESHOLD = float(os.getenv("MIN_EV_THRESHOLD", 2.0))

# CORS Configuration
# Para desarrollo local
DEFAULT_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8081",
    "exp://localhost:8081",
    "http://192.168.1.100:8081",  # Para testing en red local
]

# Añadir orígenes de producción desde variable de entorno
# Formato: CORS_ORIGINS="https://tu-app.railway.app,https://tu-dominio.com"
ADDITIONAL_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")
CORS_ORIGINS = DEFAULT_ORIGINS + [origin.strip() for origin in ADDITIONAL_ORIGINS if origin.strip()]

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "logs/betting_analyzer.log"
