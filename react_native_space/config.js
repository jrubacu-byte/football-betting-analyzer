import Constants from 'expo-constants';

// Configuración de entornos
const ENV = {
  dev: {
    apiUrl: 'http://localhost:8000/api',
    environment: 'development',
    logLevel: 'info',
  },
  staging: {
    apiUrl: 'https://tu-proyecto-staging.up.railway.app/api',
    environment: 'staging',
    logLevel: 'warn',
  },
  prod: {
    apiUrl: 'https://football-betting-analyzer-production.up.railway.app/api',
    environment: 'production',
    logLevel: 'error',
  },
};

/**
 * Obtiene las variables de entorno según el contexto de ejecución
 * 
 * Prioridad:
 * 1. Variable de entorno API_ENV (de EAS Build)
 * 2. __DEV__ flag (React Native)
 * 3. Fallback a production
 */
const getEnvVars = () => {
  // Leer variable de entorno de EAS Build
  const apiEnv = Constants.expoConfig?.extra?.API_ENV || 
                 Constants.manifest?.extra?.API_ENV;
  
  // Si hay API_ENV explícito, usarlo
  if (apiEnv === 'development') {
    return ENV.dev;
  } else if (apiEnv === 'staging') {
    return ENV.staging;
  } else if (apiEnv === 'production') {
    return ENV.prod;
  }
  
  // Fallback: usar __DEV__ para determinar entorno
  if (__DEV__) {
    return ENV.dev;
  }
  
  // Default: producción
  return ENV.prod;
};

const config = getEnvVars();

// Log del entorno actual (solo en desarrollo)
if (__DEV__) {
  console.log('📡 API Config:', {
    environment: config.environment,
    apiUrl: config.apiUrl,
  });
}

export default config;
