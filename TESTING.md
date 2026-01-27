# 🧪 Guía de Testing

## Testing del Backend

### 1. Test de Health Check

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "environment": "development",
  "version": "1.0.0"
}
```

### 2. Test de Análisis

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "match_name": "Ajax vs Olympiacos",
    "odds": {
      "home_win": 1.50,
      "draw": 3.50,
      "away_win": 6.00
    },
    "bankroll": 1000
  }'
```

### 3. Test de Conexión Móvil

En la app móvil, abre la consola y verifica:
```javascript
// Debería mostrar logs de conexión
[API] POST http://localhost:8000/api/analyze
[API] Response 200 from http://localhost:8000/api/analyze
```

## Testing de la App Móvil

### 1. Test de Formulario
- Introduce datos válidos
- Verifica que el botón se habilita
- Toca "Analizar"
- Verifica que aparece el spinner

### 2. Test de Resultados
- Verifica que se muestran las probabilidades
- Verifica que el gráfico se renderiza
- Verifica que aparece la recomendación

### 3. Test de Historial
- Guarda un análisis
- Navega a Historial
- Verifica que aparece el análisis guardado

## Casos de Error

### Backend no disponible
```
Error: Network Error
Solución: Verifica que el backend está corriendo en http://localhost:8000
```

### API URL incorrecta
```
Error: 404 Not Found
Solución: Verifica la URL en config.js
```

### LLM API Key inválida
```
Error: 401 Unauthorized
Solución: Verifica tu LLM_API_KEY en backend/.env
```
