from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from backend.routes.analysis_routes import router
from backend.config import CORS_ORIGINS, ENVIRONMENT
import logging
import os

# Configurar logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/betting_analyzer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Football Betting Analyzer API",
    description="API profesional para análisis de apuestas deportivas con EV+",
    version="1.0.0",
    docs_url="/docs" if ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if ENVIRONMENT == "development" else None,
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de hosts confiables
# En producción, Railway asigna un dominio automáticamente
allowed_hosts = ["localhost", "127.0.0.1"]
if ENVIRONMENT == "production":
    # Permitir dominios de Railway y personalizados
    railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "")
    custom_domain = os.getenv("CUSTOM_DOMAIN", "")
    if railway_domain:
        allowed_hosts.append(railway_domain)
    if custom_domain:
        allowed_hosts.append(custom_domain)
    # Permitir wildcards para subdominios
    allowed_hosts.extend(["*.railway.app", "*.up.railway.app"])

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=allowed_hosts
)

# Incluir rutas
app.include_router(router)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Football Betting Analyzer API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    from backend.config import BACKEND_HOST, BACKEND_PORT

    logger.info(f"Starting server on {BACKEND_HOST}:{BACKEND_PORT}")
    uvicorn.run(
        app,
        host=BACKEND_HOST,
        port=BACKEND_PORT,
        log_level="info"
    )
