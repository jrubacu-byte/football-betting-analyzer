#!/bin/bash

# Script para probar el backend antes de desplegar
# Uso: ./scripts/test_backend.sh

set -e  # Exit on error

echo "🧪 Backend Testing Script"
echo "========================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python instalado${NC}"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${YELLOW}Python version: $PYTHON_VERSION${NC}"

if (( $(echo "$PYTHON_VERSION < 3.11" | bc -l) )); then
    echo -e "${YELLOW}⚠️  Se recomienda Python 3.11 o superior${NC}"
fi

echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment no encontrado${NC}"
    echo "Creando virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment creado${NC}"
fi

echo -e "${GREEN}✓ Virtual environment existe${NC}"
echo ""

# Activate virtual environment
echo "Activando virtual environment..."
source venv/bin/activate

echo -e "${GREEN}✓ Virtual environment activado${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}Instalando dependencias...${NC}"
pip install -q -r backend/requirements.txt

echo -e "${GREEN}✓ Dependencias instaladas${NC}"
echo ""

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠️  backend/.env no encontrado${NC}"
    echo "Copiando desde .env.example..."
    cp backend/.env.example backend/.env
    echo -e "${RED}❗ IMPORTANTE: Edita backend/.env con tus valores reales${NC}"
    echo -e "${RED}Especialmente LLM_API_KEY${NC}"
    echo ""
fi

# Check for required environment variables
echo -e "${YELLOW}Verificando variables de entorno...${NC}"
source backend/.env 2>/dev/null || true

if [ -z "$LLM_API_KEY" ]; then
    echo -e "${RED}❌ LLM_API_KEY no está configurado en backend/.env${NC}"
    echo -e "${YELLOW}Algunas pruebas fallarán sin esta variable${NC}"
    read -p "¿Deseas continuar de todas formas? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✓ LLM_API_KEY configurado${NC}"
fi

echo ""

# Run unit tests
echo -e "${GREEN}🧪 Ejecutando tests unitarios...${NC}"
echo ""

if command -v pytest &> /dev/null; then
    pytest backend/ -v --tb=short
    TEST_RESULT=$?
else
    echo -e "${YELLOW}⚠️  pytest no instalado, instalando...${NC}"
    pip install -q pytest pytest-asyncio
    pytest backend/ -v --tb=short
    TEST_RESULT=$?
fi

echo ""

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ Todos los tests pasaron${NC}"
else
    echo -e "${RED}❌ Algunos tests fallaron${NC}"
    exit 1
fi

echo ""

# Test server startup
echo -e "${YELLOW}🚀 Probando inicio del servidor...${NC}"
echo ""

# Start server in background
python -m backend.main &
SERVER_PID=$!

echo "Servidor iniciado con PID: $SERVER_PID"
echo "Esperando 5 segundos para que el servidor inicie..."
sleep 5

# Test health endpoint
echo -e "${YELLOW}Probando health endpoint...${NC}"
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health || echo "FAILED")

if [[ $HEALTH_RESPONSE == *"healthy"* ]]; then
    echo -e "${GREEN}✓ Health check exitoso${NC}"
    echo "Respuesta: $HEALTH_RESPONSE"
else
    echo -e "${RED}❌ Health check falló${NC}"
    echo "Respuesta: $HEALTH_RESPONSE"
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

echo ""

# Test root endpoint
echo -e "${YELLOW}Probando root endpoint...${NC}"
ROOT_RESPONSE=$(curl -s http://localhost:8000/ || echo "FAILED")

if [[ $ROOT_RESPONSE == *"Football Betting Analyzer"* ]]; then
    echo -e "${GREEN}✓ Root endpoint exitoso${NC}"
else
    echo -e "${RED}❌ Root endpoint falló${NC}"
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

echo ""

# Stop server
echo "Deteniendo servidor..."
kill $SERVER_PID 2>/dev/null || true
sleep 2

echo -e "${GREEN}✓ Servidor detenido${NC}"
echo ""

# Summary
echo "═══════════════════════════════════════"
echo -e "${GREEN}✅ TODOS LOS TESTS PASARON${NC}"
echo "═══════════════════════════════════════"
echo ""
echo "El backend está listo para deployment."
echo ""
echo "Próximos pasos:"
echo "1. Despliega en Railway: ./scripts/deploy_railway.sh"
echo "2. O ejecuta localmente: python -m backend.main"
echo ""
