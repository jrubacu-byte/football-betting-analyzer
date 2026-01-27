#!/bin/bash

# Script para deployment automatizado en Railway
# Uso: ./scripts/deploy_railway.sh

set -e  # Exit on error

echo "🚂 Railway Deployment Script"
echo "=============================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo -e "${RED}❌ Railway CLI no está instalado${NC}"
    echo -e "${YELLOW}Instalando Railway CLI...${NC}"
    npm install -g @railway/cli
fi

echo -e "${GREEN}✓ Railway CLI instalado${NC}"
echo ""

# Check if logged in
echo "Verificando autenticación..."
if ! railway whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️  No estás autenticado en Railway${NC}"
    echo "Inicia sesión:"
    railway login
fi

echo -e "${GREEN}✓ Autenticado en Railway${NC}"
echo ""

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠️  No se encontró backend/.env${NC}"
    echo "Copiando desde .env.example..."
    cp backend/.env.example backend/.env
    echo -e "${RED}❗ IMPORTANTE: Edita backend/.env con tus valores reales${NC}"
    read -p "Presiona Enter cuando hayas editado el archivo..."
fi

# Test backend locally before deploying
echo -e "${YELLOW}🧪 Probando backend localmente...${NC}"
if bash scripts/test_backend.sh; then
    echo -e "${GREEN}✓ Tests pasaron correctamente${NC}"
else
    echo -e "${RED}❌ Tests fallaron${NC}"
    read -p "¿Deseas continuar con el deploy? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Deploy cancelado."
        exit 1
    fi
fi

echo ""

# Initialize Railway project if not exists
if [ ! -f "railway.json" ]; then
    echo -e "${RED}❌ railway.json no encontrado${NC}"
    exit 1
fi

echo -e "${GREEN}✓ railway.json encontrado${NC}"
echo ""

# Link to Railway project (if not already linked)
echo "Vinculando con proyecto de Railway..."
if ! railway status &> /dev/null; then
    echo -e "${YELLOW}⚠️  No vinculado a ningún proyecto${NC}"
    echo "Opciones:"
    echo "1. Vincular a proyecto existente: railway link"
    echo "2. Crear nuevo proyecto: railway init"
    read -p "¿Qué deseas hacer? (1/2): " choice
    
    if [ "$choice" = "1" ]; then
        railway link
    else
        railway init
    fi
fi

echo -e "${GREEN}✓ Vinculado a proyecto${NC}"
echo ""

# Show current environment variables
echo -e "${YELLOW}Variables de entorno actuales en Railway:${NC}"
railway variables
echo ""

# Ask if user wants to update environment variables
read -p "¿Deseas actualizar variables de entorno? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "Abriendo editor de variables..."
    railway variables --edit
fi

echo ""

# Commit changes before deploying
echo -e "${YELLOW}Verificando cambios de Git...${NC}"
if [[ -n $(git status -s) ]]; then
    echo -e "${YELLOW}⚠️  Hay cambios sin commitear${NC}"
    git status -s
    echo ""
    read -p "¿Deseas commitear estos cambios? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        read -p "Mensaje de commit: " commit_msg
        git add .
        git commit -m "$commit_msg"
        git push
        echo -e "${GREEN}✓ Cambios commiteados y pusheados${NC}"
    fi
fi

echo ""

# Deploy to Railway
echo -e "${GREEN}🚀 Desplegando a Railway...${NC}"
railway up

echo ""
echo -e "${GREEN}✅ ¡Deploy completado!${NC}"
echo ""

# Show deployment URL
echo "Obteniendo URL del deployment..."
railway status

echo ""
echo -e "${GREEN}🎉 ¡Deployment exitoso!${NC}"
echo ""
echo "Próximos pasos:"
echo "1. Verifica el health check: https://tu-url.railway.app/health"
echo "2. Prueba el endpoint de análisis"
echo "3. Actualiza la URL en react_native_space/config.js"
echo "4. Compila la app móvil con: ./scripts/build_mobile.sh"
echo ""
