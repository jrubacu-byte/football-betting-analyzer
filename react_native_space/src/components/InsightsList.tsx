import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface RefereeInfo {
  name: string;
  avg_cards: number;
  tendency: string;
}

interface Props {
  insights: string[];
  refereeInfo: RefereeInfo;
}

const InsightsList: React.FC<Props> = ({ insights, refereeInfo }) => {
  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <Text style={styles.headerIcon}>💡</Text>
        <Text style={styles.headerTitle}>Datos Clave</Text>
      </View>
      
      {insights && insights.length > 0 && (
        <View style={styles.section}>
          {insights.map((insight, index) => (
            <View key={index} style={styles.insightRow}>
              <Text style={styles.bullet}>•</Text>
              <Text style={styles.insightText}>{insight}</Text>
            </View>
          ))}
        </View>
      )}
      
      {refereeInfo && (
        <View style={styles.refereeSection}>
          <View style={styles.divider} />
          <Text style={styles.refereeSectionTitle}>🟨 Información del Árbitro</Text>
          
          <View style={styles.refereeInfo}>
            <View style={styles.refereeRow}>
              <Text style={styles.refereeLabel}>Nombre:</Text>
              <Text style={styles.refereeValue}>{refereeInfo.name}</Text>
            </View>
            
            <View style={styles.refereeRow}>
              <Text style={styles.refereeLabel}>Tarjetas promedio:</Text>
              <Text style={styles.refereeValue}>{refereeInfo.avg_cards.toFixed(1)}</Text>
            </View>
            
            <View style={styles.refereeRow}>
              <Text style={styles.refereeLabel}>Tendencia:</Text>
              <Text style={[
                styles.refereeValue,
                styles.tendencyBadge,
                refereeInfo.tendency.toLowerCase().includes('estricto') && styles.strictBadge,
                refereeInfo.tendency.toLowerCase().includes('permisivo') && styles.permissiveBadge,
              ]}>
                {refereeInfo.tendency}
              </Text>
            </View>
          </View>
        </View>
      )}
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
  section: {
    marginBottom: 8,
  },
  insightRow: {
    flexDirection: 'row',
    marginBottom: 12,
  },
  bullet: {
    color: '#3498db',
    fontSize: 16,
    marginRight: 8,
    marginTop: 2,
  },
  insightText: {
    flex: 1,
    color: '#ecf0f1',
    fontSize: 14,
    lineHeight: 20,
  },
  refereeSection: {
    marginTop: 8,
  },
  divider: {
    height: 1,
    backgroundColor: '#2c2c2c',
    marginVertical: 16,
  },
  refereeSectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ecf0f1',
    marginBottom: 12,
  },
  refereeInfo: {
    paddingLeft: 8,
  },
  refereeRow: {
    flexDirection: 'row',
    marginBottom: 8,
    alignItems: 'center',
  },
  refereeLabel: {
    color: '#95a5a6',
    fontSize: 14,
    width: 150,
  },
  refereeValue: {
    color: '#ecf0f1',
    fontSize: 14,
    fontWeight: '600',
    flex: 1,
  },
  tendencyBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
    overflow: 'hidden',
  },
  strictBadge: {
    backgroundColor: '#e74c3c',
  },
  permissiveBadge: {
    backgroundColor: '#27ae60',
  },
});

export default InsightsList;
