import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { formatOdds, formatEV, formatMarketName } from '../utils/formatters';

interface MarketAnalysis {
  market: string;
  bookmaker_odds: number;
  fair_odds: number;
  ev_percent: number;
}

interface Props {
  marketAnalysis: MarketAnalysis[];
}

const MarketAnalysisCard: React.FC<Props> = ({ marketAnalysis }) => {
  if (!marketAnalysis || marketAnalysis.length === 0) {
    return null;
  }

  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <Text style={styles.headerIcon}>📊</Text>
        <Text style={styles.headerTitle}>Análisis de Mercados</Text>
      </View>
      
      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
        <View style={styles.table}>
          {/* Table Header */}
          <View style={styles.tableRow}>
            <Text style={[styles.tableCell, styles.headerCell, styles.marketColumn]}>Mercado</Text>
            <Text style={[styles.tableCell, styles.headerCell, styles.oddsColumn]}>Casa</Text>
            <Text style={[styles.tableCell, styles.headerCell, styles.oddsColumn]}>Justa</Text>
            <Text style={[styles.tableCell, styles.headerCell, styles.evColumn]}>EV</Text>
          </View>
          
          {/* Table Rows */}
          {marketAnalysis.map((item, index) => {
            const evFormatted = formatEV(item.ev_percent);
            const isHighlight = item.ev_percent >= 3;
            
            return (
              <View 
                key={index} 
                style={[
                  styles.tableRow, 
                  isHighlight && styles.highlightRow,
                  index === marketAnalysis.length - 1 && styles.lastRow
                ]}
              >
                <Text style={[styles.tableCell, styles.marketColumn, styles.marketText]}>
                  {formatMarketName(item.market)}
                </Text>
                <Text style={[styles.tableCell, styles.oddsColumn, styles.valueText]}>
                  {formatOdds(item.bookmaker_odds)}
                </Text>
                <Text style={[styles.tableCell, styles.oddsColumn, styles.valueText]}>
                  {formatOdds(item.fair_odds)}
                </Text>
                <Text 
                  style={[
                    styles.tableCell, 
                    styles.evColumn, 
                    styles.valueText,
                    { color: evFormatted.color }
                  ]}
                >
                  {evFormatted.text}
                </Text>
              </View>
            );
          })}
        </View>
      </ScrollView>
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
  table: {
    minWidth: '100%',
  },
  tableRow: {
    flexDirection: 'row',
    borderBottomWidth: 1,
    borderBottomColor: '#2c2c2c',
    paddingVertical: 12,
  },
  lastRow: {
    borderBottomWidth: 0,
  },
  highlightRow: {
    backgroundColor: 'rgba(39, 174, 96, 0.1)',
  },
  tableCell: {
    paddingHorizontal: 8,
  },
  headerCell: {
    fontWeight: 'bold',
    color: '#95a5a6',
    fontSize: 14,
  },
  marketColumn: {
    flex: 2,
    minWidth: 150,
  },
  oddsColumn: {
    flex: 1,
    minWidth: 70,
    textAlign: 'center',
  },
  evColumn: {
    flex: 1,
    minWidth: 80,
    textAlign: 'center',
  },
  marketText: {
    color: '#ecf0f1',
    fontSize: 14,
  },
  valueText: {
    color: '#ecf0f1',
    fontSize: 14,
    fontWeight: '600',
  },
});

export default MarketAnalysisCard;
