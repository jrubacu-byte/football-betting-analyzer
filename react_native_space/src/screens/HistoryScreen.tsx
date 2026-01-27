import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  RefreshControl,
  Alert,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useFocusEffect } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../navigation/types';
import { getAnalysisHistory, clearHistory, type AnalysisResult } from '../services/api';
import { formatDate, formatOdds, formatEV, formatMarketName } from '../utils/formatters';

type HistoryScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'HistoryScreen'>;

interface Props {
  navigation: HistoryScreenNavigationProp;
}

const HistoryScreen: React.FC<Props> = ({ navigation }) => {
  const [history, setHistory] = useState<AnalysisResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadHistory = async () => {
    try {
      const data = await getAnalysisHistory();
      setHistory(data);
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useFocusEffect(
    useCallback(() => {
      loadHistory();
    }, [])
  );

  const handleRefresh = () => {
    setRefreshing(true);
    loadHistory();
  };

  const handleClearHistory = () => {
    Alert.alert(
      'Confirmar',
      '¿Estás seguro de que quieres borrar todo el historial?',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Borrar',
          style: 'destructive',
          onPress: async () => {
            try {
              await clearHistory();
              setHistory([]);
              Alert.alert('Éxito', 'Historial borrado');
            } catch (error: any) {
              Alert.alert('Error', error.message);
            }
          },
        },
      ]
    );
  };

  const handleItemPress = (analysis: AnalysisResult) => {
    navigation.navigate('AnalysisScreen', { analysis });
  };

  const renderItem = ({ item }: { item: AnalysisResult }) => {
    const evFormatted = formatEV(item.recommended_bet.ev_percent);

    return (
      <TouchableOpacity
        style={styles.historyItem}
        onPress={() => handleItemPress(item)}
        activeOpacity={0.7}
      >
        <View style={styles.itemHeader}>
          <Text style={styles.matchName} numberOfLines={1}>
            {item.match_name}
          </Text>
          <Text style={styles.timestamp}>
            {item.timestamp ? formatDate(item.timestamp) : '-'}
          </Text>
        </View>

        <View style={styles.itemContent}>
          <View style={styles.betInfo}>
            <Text style={styles.betLabel}>Apuesta recomendada</Text>
            <Text style={styles.betMarket}>
              {formatMarketName(item.recommended_bet.market)}
            </Text>
            <Text style={styles.betOdds}>
              Cuota: {formatOdds(item.recommended_bet.odds)}
            </Text>
          </View>

          <View style={[styles.evBadge, { backgroundColor: evFormatted.color }]}>
            <Text style={styles.evText}>{evFormatted.text}</Text>
          </View>
        </View>
      </TouchableOpacity>
    );
  };

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Text style={styles.emptyIcon}>📋</Text>
      <Text style={styles.emptyTitle}>No hay análisis guardados</Text>
      <Text style={styles.emptySubtitle}>
        Los análisis que guardes aparecerán aquí
      </Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <StatusBar style="light" />
      
      <View style={styles.header}>
        <Text style={styles.title}>Historial de Análisis</Text>
        {history.length > 0 && (
          <TouchableOpacity onPress={handleClearHistory}>
            <Text style={styles.clearButton}>Limpiar</Text>
          </TouchableOpacity>
        )}
      </View>

      <FlatList
        data={history}
        renderItem={renderItem}
        keyExtractor={(item, index) => `${item.match_name}-${index}`}
        contentContainerStyle={[
          styles.listContent,
          history.length === 0 && styles.listContentEmpty,
        ]}
        ListEmptyComponent={renderEmptyState}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={handleRefresh}
            tintColor="#3498db"
          />
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f0f0f',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingTop: 60,
    backgroundColor: '#1e1e1e',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ecf0f1',
  },
  clearButton: {
    color: '#e74c3c',
    fontSize: 16,
    fontWeight: '600',
  },
  listContent: {
    padding: 16,
  },
  listContentEmpty: {
    flex: 1,
  },
  historyItem: {
    backgroundColor: '#1e1e1e',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
  },
  itemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  matchName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ecf0f1',
    flex: 1,
    marginRight: 8,
  },
  timestamp: {
    fontSize: 12,
    color: '#95a5a6',
  },
  itemContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  betInfo: {
    flex: 1,
  },
  betLabel: {
    fontSize: 12,
    color: '#95a5a6',
    marginBottom: 4,
  },
  betMarket: {
    fontSize: 14,
    color: '#3498db',
    fontWeight: '600',
    marginBottom: 2,
  },
  betOdds: {
    fontSize: 14,
    color: '#ecf0f1',
  },
  evBadge: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 6,
  },
  evText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 80,
  },
  emptyIcon: {
    fontSize: 64,
    marginBottom: 16,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#ecf0f1',
    marginBottom: 8,
  },
  emptySubtitle: {
    fontSize: 14,
    color: '#95a5a6',
    textAlign: 'center',
  },
});

export default HistoryScreen;
