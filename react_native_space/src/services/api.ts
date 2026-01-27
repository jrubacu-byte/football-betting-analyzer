import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Use environment variable for API base URL
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL 
  ? `${process.env.EXPO_PUBLIC_API_URL}api`
  : 'http://localhost:8000/api';

interface Odds {
  home_win: number;
  draw: number;
  away_win: number;
  over_2_5?: number;
  btts_yes?: number;
}

interface MatchData {
  match_name: string;
  odds: Odds;
  bankroll: number;
}

interface RecommendedBet {
  market: string;
  odds: number;
  ev_percent: number;
  suggested_stake: number;
  expected_profit: number;
}

interface MarketAnalysis {
  market: string;
  bookmaker_odds: number;
  fair_odds: number;
  ev_percent: number;
}

interface Probabilities {
  home_win: number;
  draw: number;
  away_win: number;
}

interface RefereeInfo {
  name: string;
  avg_cards: number;
  tendency: string;
}

export interface AnalysisResult {
  match_name: string;
  recommended_bet: RecommendedBet;
  probabilities: Probabilities;
  market_analysis: MarketAnalysis[];
  other_opportunities?: RecommendedBet[];
  key_insights: string[];
  referee_info: RefereeInfo;
  timestamp?: string;
}

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeMatch = async (matchData: MatchData): Promise<AnalysisResult> => {
  try {
    console.log('Sending request to:', `${API_BASE_URL}/analyze`);
    console.log('Request payload:', JSON.stringify(matchData, null, 2));
    
    const response = await apiClient.post('/analyze', matchData);
    
    console.log('Response status:', response.status);
    console.log('Response data:', JSON.stringify(response.data, null, 2));
    
    return response.data;
  } catch (error: any) {
    console.error('API Error:', error);
    if (error.response) {
      console.error('Error response:', error.response.data);
      console.error('Error status:', error.response.status);
      throw new Error(`Error del servidor: ${error.response.data?.detail || error.response.statusText}`);
    } else if (error.request) {
      console.error('No response received:', error.request);
      throw new Error('No se pudo conectar con el servidor. Verifica que el backend esté ejecutándose.');
    } else {
      console.error('Error message:', error.message);
      throw new Error(`Error: ${error.message}`);
    }
  }
};

export const saveAnalysisToHistory = async (analysis: AnalysisResult): Promise<void> => {
  try {
    const analysisWithTimestamp = {
      ...analysis,
      timestamp: new Date().toISOString(),
    };
    
    const existingHistory = await getAnalysisHistory();
    const newHistory = [analysisWithTimestamp, ...existingHistory];
    
    // Keep only last 50 analyses
    const limitedHistory = newHistory.slice(0, 50);
    
    await AsyncStorage.setItem('analysis_history', JSON.stringify(limitedHistory));
  } catch (error) {
    console.error('Error saving to history:', error);
    throw new Error('No se pudo guardar el análisis en el historial');
  }
};

export const getAnalysisHistory = async (): Promise<AnalysisResult[]> => {
  try {
    const historyJson = await AsyncStorage.getItem('analysis_history');
    if (!historyJson) {
      return [];
    }
    return JSON.parse(historyJson);
  } catch (error) {
    console.error('Error reading history:', error);
    return [];
  }
};

export const clearHistory = async (): Promise<void> => {
  try {
    await AsyncStorage.removeItem('analysis_history');
  } catch (error) {
    console.error('Error clearing history:', error);
    throw new Error('No se pudo limpiar el historial');
  }
};

export const checkServerHealth = async (): Promise<boolean> => {
  try {
    const response = await apiClient.get('/ping');
    return response.status === 200;
  } catch (error) {
    return false;
  }
};
