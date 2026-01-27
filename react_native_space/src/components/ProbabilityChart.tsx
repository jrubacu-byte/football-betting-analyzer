import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { PieChart } from 'react-native-chart-kit';

interface Probabilities {
  home_win: number;
  draw: number;
  away_win: number;
}

interface Props {
  probabilities: Probabilities;
}

const ProbabilityChart: React.FC<Props> = ({ probabilities }) => {
  const screenWidth = Dimensions.get('window').width;
  
  const chartData = [
    {
      name: 'Local',
      probability: probabilities.home_win,
      color: '#27ae60',
      legendFontColor: '#ecf0f1',
      legendFontSize: 14,
    },
    {
      name: 'Empate',
      probability: probabilities.draw,
      color: '#95a5a6',
      legendFontColor: '#ecf0f1',
      legendFontSize: 14,
    },
    {
      name: 'Visitante',
      probability: probabilities.away_win,
      color: '#e74c3c',
      legendFontColor: '#ecf0f1',
      legendFontSize: 14,
    },
  ];

  const chartConfig = {
    color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    labelColor: (opacity = 1) => `rgba(236, 240, 241, ${opacity})`,
  };

  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <Text style={styles.headerIcon}>📈</Text>
        <Text style={styles.headerTitle}>Probabilidades 1X2</Text>
      </View>
      
      <PieChart
        data={chartData}
        width={screenWidth - 80}
        height={220}
        chartConfig={chartConfig}
        accessor="probability"
        backgroundColor="transparent"
        paddingLeft="15"
        absolute
      />
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
});

export default ProbabilityChart;
