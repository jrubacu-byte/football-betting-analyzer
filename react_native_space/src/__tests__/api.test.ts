import AsyncStorage from '@react-native-async-storage/async-storage';
import { saveAnalysisToHistory, getAnalysisHistory, clearHistory } from '../services/api';
import type { AnalysisResult } from '../services/api';

const mockAnalysis: AnalysisResult = {
  match_name: 'Test Match',
  recommended_bet: {
    market: 'home_win',
    odds: 2.5,
    ev_percent: 5.5,
    suggested_stake: 50,
    expected_profit: 25,
  },
  probabilities: {
    home_win: 45,
    draw: 30,
    away_win: 25,
  },
  market_analysis: [],
  key_insights: ['Test insight'],
  referee_info: {
    name: 'Test Referee',
    avg_cards: 4.5,
    tendency: 'Estricto',
  },
};

describe('API Service', () => {
  beforeEach(() => {
    AsyncStorage.clear();
  });

  describe('saveAnalysisToHistory', () => {
    it('should save analysis to AsyncStorage', async () => {
      await saveAnalysisToHistory(mockAnalysis);
      const history = await getAnalysisHistory();
      
      expect(history).toHaveLength(1);
      expect(history[0].match_name).toBe('Test Match');
      expect(history[0].timestamp).toBeDefined();
    });

    it('should prepend new analysis to existing history', async () => {
      await saveAnalysisToHistory({ ...mockAnalysis, match_name: 'Match 1' });
      await saveAnalysisToHistory({ ...mockAnalysis, match_name: 'Match 2' });
      
      const history = await getAnalysisHistory();
      expect(history).toHaveLength(2);
      expect(history[0].match_name).toBe('Match 2');
      expect(history[1].match_name).toBe('Match 1');
    });

    it('should limit history to 50 items', async () => {
      for (let i = 0; i < 60; i++) {
        await saveAnalysisToHistory({ ...mockAnalysis, match_name: `Match ${i}` });
      }
      
      const history = await getAnalysisHistory();
      expect(history).toHaveLength(50);
    });
  });

  describe('getAnalysisHistory', () => {
    it('should return empty array when no history', async () => {
      const history = await getAnalysisHistory();
      expect(history).toEqual([]);
    });

    it('should return saved history', async () => {
      await saveAnalysisToHistory(mockAnalysis);
      const history = await getAnalysisHistory();
      
      expect(history).toHaveLength(1);
      expect(history[0].match_name).toBe('Test Match');
    });
  });

  describe('clearHistory', () => {
    it('should clear all history', async () => {
      await saveAnalysisToHistory(mockAnalysis);
      await clearHistory();
      
      const history = await getAnalysisHistory();
      expect(history).toEqual([]);
    });
  });
});
