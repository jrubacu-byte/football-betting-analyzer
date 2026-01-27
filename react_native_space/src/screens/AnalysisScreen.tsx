import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RouteProp } from '@react-navigation/native';
import type { RootStackParamList } from '../navigation/types';
import { saveAnalysisToHistory } from '../services/api';
import RecommendationCard from '../components/RecommendationCard';
import ProbabilityChart from '../components/ProbabilityChart';
import MarketAnalysisCard from '../components/MarketAnalysisCard';
import InsightsList from '../components/InsightsList';
import { formatDate } from '../utils/formatters';

type AnalysisScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'AnalysisScreen'>;
type AnalysisScreenRouteProp = RouteProp<RootStackParamList, 'AnalysisScreen'>;

interface Props {
  navigation: AnalysisScreenNavigationProp;
  route: AnalysisScreenRouteProp;
}

const AnalysisScreen: React.FC<Props> = ({ navigation, route }) => {
  const { analysis } = route.params;
  const [saved, setSaved] = useState(false);

  const handleSaveToHistory = async () => {
    try {
      await saveAnalysisToHistory(analysis);
      setSaved(true);
      Alert.alert('Éxito', 'Análisis guardado en el historial');
    } catch (error: any) {
      Alert.alert('Error', error.message || 'No se pudo guardar el análisis');
    }
  };

  const handleNewAnalysis = () => {
    navigation.navigate('InputScreen');
  };

  return (
    <View style={styles.container}>
      <StatusBar style="light" />
      <ScrollView 
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
      >
        <View style={styles.header}>
          <Text style={styles.matchName}>{analysis.match_name}</Text>
          {analysis.timestamp && (
            <Text style={styles.timestamp}>{formatDate(analysis.timestamp)}</Text>
          )}
        </View>

        <RecommendationCard recommendation={analysis.recommended_bet} />

        <ProbabilityChart probabilities={analysis.probabilities} />

        <MarketAnalysisCard marketAnalysis={analysis.market_analysis} />

        {analysis.other_opportunities && analysis.other_opportunities.length > 0 && (
          <View style={styles.card}>
            <View style={styles.cardHeader}>
              <Text style={styles.cardIcon}>🎲</Text>
              <Text style={styles.cardTitle}>Otras Oportunidades</Text>
            </View>
            {analysis.other_opportunities.map((opportunity, index) => (
              <View key={index} style={styles.opportunityItem}>
                <RecommendationCard recommendation={opportunity} />
              </View>
            ))}
          </View>
        )}

        <InsightsList 
          insights={analysis.key_insights} 
          refereeInfo={analysis.referee_info} 
        />

        <View style={styles.actions}>
          <TouchableOpacity
            style={[styles.button, styles.saveButton, saved && styles.buttonDisabled]}
            onPress={handleSaveToHistory}
            disabled={saved}
          >
            <Text style={styles.buttonText}>
              {saved ? '✓ Guardado' : 'Guardar en Historial'}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.newButton]}
            onPress={handleNewAnalysis}
          >
            <Text style={styles.buttonText}>Nuevo Análisis</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f0f0f',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  header: {
    marginTop: 16,
    marginBottom: 24,
  },
  matchName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ecf0f1',
    textAlign: 'center',
    marginBottom: 8,
  },
  timestamp: {
    fontSize: 14,
    color: '#95a5a6',
    textAlign: 'center',
  },
  card: {
    backgroundColor: '#1e1e1e',
    borderRadius: 12,
    padding: 20,
    marginVertical: 8,
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  cardIcon: {
    fontSize: 24,
    marginRight: 8,
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ecf0f1',
  },
  opportunityItem: {
    marginTop: 8,
  },
  actions: {
    marginTop: 24,
    gap: 12,
  },
  button: {
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
  },
  saveButton: {
    backgroundColor: '#27ae60',
  },
  newButton: {
    backgroundColor: '#3498db',
  },
  buttonDisabled: {
    backgroundColor: '#5a7a5a',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default AnalysisScreen;
