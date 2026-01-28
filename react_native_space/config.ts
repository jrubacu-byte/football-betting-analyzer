import Constants from 'expo-constants';

// Environment configuration types
interface EnvConfig {
  apiUrl: string;
  environment: 'development' | 'staging' | 'production';
  logLevel: 'info' | 'warn' | 'error';
}

// Environment configurations
const ENV: Record<'dev' | 'staging' | 'prod', EnvConfig> = {
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
 * Gets environment variables based on execution context
 * 
 * Priority:
 * 1. API_ENV environment variable (from EAS Build)
 * 2. __DEV__ flag (React Native)
 * 3. Fallback to production
 */
const getEnvVars = (): EnvConfig => {
  // Read environment variable from EAS Build
  const apiEnv = Constants.expoConfig?.extra?.API_ENV || 
                 Constants.manifest?.extra?.API_ENV;
  
  // If explicit API_ENV is set, use it
  if (apiEnv === 'development') {
    return ENV.dev;
  } else if (apiEnv === 'staging') {
    return ENV.staging;
  } else if (apiEnv === 'production') {
    return ENV.prod;
  }
  
  // Fallback: use __DEV__ to determine environment
  if (__DEV__) {
    return ENV.dev;
  }
  
  // Default: production
  return ENV.prod;
};

const config = getEnvVars();

// Log current environment (only in development)
if (__DEV__) {
  console.log('📡 API Config:', {
    environment: config.environment,
    apiUrl: config.apiUrl,
  });
}

export default config;
