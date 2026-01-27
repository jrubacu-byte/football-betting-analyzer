import type { AnalysisResult } from '../services/api';

export type RootStackParamList = {
  InputScreen: undefined;
  AnalysisScreen: { analysis: AnalysisResult };
};

export type TabParamList = {
  AnalyzeTab: undefined;
  HistoryScreen: undefined;
};
