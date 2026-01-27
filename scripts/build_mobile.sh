#!/bin/bash

# Script para compilar app móvil con Expo EAS Build
# Uso: ./scripts/build_mobile.sh [android|ios|all]

set -e  # Exit on error

echo "📱 Expo EAS Build Script"
echo "========================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if eas-cli is installed
if ! command -v eas &> /dev/null; then
    echo -e "${RED}❌ EAS CLI no está instalado${NC}"
    echo -e "${YELLOW}Instalando EAS CLI...${NC}"
    npm install -g eas-cli
fi

echo -e "${GREEN}✓ EAS CLI instalado${NC}"
echo ""

# Check if logged in
echo "Verificando autenticación de Expo..."
if ! eas whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️  No estás autenticado en Expo${NC}"
    echo "Inicia sesión:"
    eas login
fi

echo -e "${GREEN}✓ Autenticado en Expo${NC}"
echo ""

# Navigate to mobile app directory
cd react_native_space

echo -e "${YELLOW}Directorio actual: $(pwd)${NC}"
echo ""

# Check if eas.json exists
if [ ! -f "eas.json" ]; then
    echo -e "${RED}❌ eas.json no encontrado${NC}"
    echo "Ejecutando eas build:configure..."
    eas build:configure
fi

echo -e "${GREEN}✓ eas.json encontrado${NC}"
echo ""

# Check if app.json is properly configured
if ! grep -q "projectId" app.json; then
    echo -e "${RED}❌ app.json no tiene projectId configurado${NC}"
    echo -e "${YELLOW}Por favor, configura el projectId en app.json${NC}"
    echo "Ve a: https://expo.dev y crea un nuevo proyecto"
    exit 1
fi

echo -e "${GREEN}✓ app.json configurado correctamente${NC}"
echo ""

# Check backend URL configuration
echo -e "${YELLOW}Verificando configuración de backend URL...${NC}"
if grep -q "localhost:8000" config.js; then
    echo -e "${RED}⚠️  ADVERTENCIA: config.js todavía usa localhost${NC}"
    echo -e "${YELLOW}Asegúrate de actualizar la URL de producción antes de compilar${NC}"
    echo ""
    cat config.js | grep -A 3 "prod:"
    echo ""
    read -p "¿Deseas continuar? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Build cancelado. Actualiza config.js primero."
        exit 1
    fi
fi

echo ""

# Determine platform
PLATFORM=${1:-"android"}  # Default to android

if [ "$PLATFORM" != "android" ] && [ "$PLATFORM" != "ios" ] && [ "$PLATFORM" != "all" ]; then
    echo -e "${RED}❌ Plataforma inválida: $PLATFORM${NC}"
    echo "Uso: ./scripts/build_mobile.sh [android|ios|all]"
    exit 1
fi

echo -e "${BLUE}Plataforma seleccionada: $PLATFORM${NC}"
echo ""

# Determine profile
echo "Selecciona el perfil de build:"
echo "1. preview (APK/Ad Hoc - Para testing)"
echo "2. production (AAB/IPA - Para stores)"
echo "3. development (Development build)"
read -p "Selecciona (1/2/3): " profile_choice

case $profile_choice in
    1)
        PROFILE="preview"
        ;;
    2)
        PROFILE="production"
        ;;
    3)
        PROFILE="development"
        ;;
    *)
        echo -e "${RED}❌ Opción inválida${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}Perfil seleccionado: $PROFILE${NC}"
echo ""

# Check if iOS build requires Apple account
if [ "$PLATFORM" = "ios" ] || [ "$PLATFORM" = "all" ]; then
    echo -e "${YELLOW}⚠️  NOTA: iOS builds requieren Apple Developer Account ($99/año)${NC}"
    read -p "¿Tienes Apple Developer Account configurado? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        if [ "$PLATFORM" = "all" ]; then
            echo "Compilando solo para Android..."
            PLATFORM="android"
        else
            echo "Build cancelado."
            exit 1
        fi
    fi
fi

echo ""

# Run build
echo -e "${GREEN}🚀 Iniciando build...${NC}"
echo -e "${YELLOW}Plataforma: $PLATFORM${NC}"
echo -e "${YELLOW}Perfil: $PROFILE${NC}"
echo ""
echo "Este proceso puede tomar 10-20 minutos..."
echo ""

eas build --platform $PLATFORM --profile $PROFILE --non-interactive

echo ""
echo -e "${GREEN}✅ ¡Build completado!${NC}"
echo ""

# Show build list
echo "Últimos builds:"
eas build:list --limit 5

echo ""
echo -e "${GREEN}🎉 ¡Build exitoso!${NC}"
echo ""
echo "Próximos pasos:"
echo "1. Descarga el APK/IPA desde el link proporcionado"
echo "2. Instálalo en tu dispositivo"
echo "3. Prueba la conexión con el backend"
echo ""
echo "Para ver todos los builds: eas build:list"
echo "Para descargar un build específico, usa el link de la web de Expo"
echo ""

# Return to root directory
cd ..
