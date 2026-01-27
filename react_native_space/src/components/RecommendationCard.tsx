import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { formatOdds, formatEV, formatStake, formatMarketName } from '../utils/formatters';

interface RecommendedBet {
  market: string;
  odds: number;
  ev_percent: number;
  suggested_stake: number;
  expected_profit: number;
}

interface Props {
  recommendation: RecommendedBet;
}

const RecommendationCard: React.FC<Props> = ({ recommendation }) => {
  const evFormatted = formatEV(recommendation.ev_percent);
  
  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <Text style={styles.headerIcon}>🎯</Text>
        <Text style={styles.headerTitle}>Apuesta Recomendada</Text>
      </View>
      
      <View style={styles.mainInfo}>
        <Text style={styles.marketLabel}>Mercado</Text>
        <Text style={styles.marketValue}>{formatMarketName(recommendation.market)}</Text>
      </View>
      
      <View style={styles.statsRow}>
        <View style={styles.statItem}>
          <Text style={styles.statLabel}>Cuota</Text>
          <Text style={styles.statValue}>{formatOdds(recommendation.odds)}</Text>
        </View>
        
        <View style={styles.statItem}>
          <Text style={styles.statLabel}>Valor Esperado</Text>
          <View style={[styles.evBadge, { backgroundColor: evFormatted.color }]}>
            <Text style={styles.evText}>{evFormatted.text}</Text>
          </View>
        </View>
      </View>
      
      <View style={styles.divider} />
      
      <View style={styles.stakeRow}>
        <View style={styles.stakeItem}>
          <Text style={styles.stakeLabel}>Stake Sugerido</Text>
          <Text style={styles.stakeValue}>{formatStake(recommendation.suggested_stake)}</Text>
        </View>
        
        <View style={styles.stakeItem}>
          <Text style={styles.stakeLabel}>Beneficio Esperado</Text>
          <Text style={[styles.stakeValue, styles.profitValue]}>
            {formatStake(recommendation.expected_profit)}
          </Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
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
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  headerIcon: {
    fontSize: 24,
    marginRight: 8,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ecf0f1',
  },
  mainInfo: {
    marginBottom: 16,
  },
  marketLabel: {
    fontSize: 14,
    color: '#95a5a6',
    marginBottom: 4,
  },
  marketValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#3498db',
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  statItem: {
    flex: 1,
  },
  statLabel: {
    fontSize: 14,
    color: '#95a5a6',
    marginBottom: 4,
  },
  statValue: {
    fontSize: 20,
    fontWeight: '600',
    color: '#ecf0f1',
  },
  evBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
  },
  evText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  divider: {
    height: 1,
    backgroundColor: '#2c2c2c',
    marginVertical: 16,
  },
  stakeRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  stakeItem: {
    flex: 1,
  },
  stakeLabel: {
    fontSize: 14,
    color: '#95a5a6',
    marginBottom: 4,
  },
  stakeValue: {
    fontSize: 18,
    fontWeight: '600',
    color: '#ecf0f1',
  },
  profitValue: {
    color: '#27ae60',
  },
});

export default RecommendationCard;
