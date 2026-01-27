import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { analyzeMatch } from '../services/api';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../navigation/types';

type InputScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'InputScreen'>;

interface Props {
  navigation: InputScreenNavigationProp;
}

const InputScreen: React.FC<Props> = ({ navigation }) => {
  const [matchName, setMatchName] = useState('');
  const [homeWin, setHomeWin] = useState('');
  const [draw, setDraw] = useState('');
  const [awayWin, setAwayWin] = useState('');
  const [over25, setOver25] = useState('');
  const [bttsYes, setBttsYes] = useState('');
  const [bankroll, setBankroll] = useState('');
  const [loading, setLoading] = useState(false);

  const validateInputs = (): boolean => {
    if (!matchName.trim()) {
      Alert.alert('Error', 'Por favor ingresa el nombre del partido');
      return false;
    }

    const homeWinNum = parseFloat(homeWin);
    const drawNum = parseFloat(draw);
    const awayWinNum = parseFloat(awayWin);
    const bankrollNum = parseFloat(bankroll);

    if (isNaN(homeWinNum) || homeWinNum <= 1.0) {
      Alert.alert('Error', 'La cuota de victoria local debe ser mayor a 1.0');
      return false;
    }

    if (isNaN(drawNum) || drawNum <= 1.0) {
      Alert.alert('Error', 'La cuota de empate debe ser mayor a 1.0');
      return false;
    }

    if (isNaN(awayWinNum) || awayWinNum <= 1.0) {
      Alert.alert('Error', 'La cuota de victoria visitante debe ser mayor a 1.0');
      return false;
    }

    if (isNaN(bankrollNum) || bankrollNum <= 0) {
      Alert.alert('Error', 'El bankroll debe ser mayor a 0');
      return false;
    }

    if (over25) {
      const over25Num = parseFloat(over25);
      if (isNaN(over25Num) || over25Num <= 1.0) {
        Alert.alert('Error', 'La cuota de Más de 2.5 debe ser mayor a 1.0');
        return false;
      }
    }

    if (bttsYes) {
      const bttsYesNum = parseFloat(bttsYes);
      if (isNaN(bttsYesNum) || bttsYesNum <= 1.0) {
        Alert.alert('Error', 'La cuota de Ambos equipos marcan debe ser mayor a 1.0');
        return false;
      }
    }

    return true;
  };

  const handleAnalyze = async () => {
    if (!validateInputs()) {
      return;
    }

    setLoading(true);

    try {
      const matchData = {
        match_name: matchName.trim(),
        odds: {
          home_win: parseFloat(homeWin),
          draw: parseFloat(draw),
          away_win: parseFloat(awayWin),
          ...(over25 && { over_2_5: parseFloat(over25) }),
          ...(bttsYes && { btts_yes: parseFloat(bttsYes) }),
        },
        bankroll: parseFloat(bankroll),
      };

      const analysis = await analyzeMatch(matchData);
      
      navigation.navigate('AnalysisScreen', { analysis });
    } catch (error: any) {
      Alert.alert('Error', error.message || 'No se pudo completar el análisis');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 64 : 0}
    >
      <StatusBar style="light" />
      <ScrollView 
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.header}>
          <Text style={styles.headerIcon}>⚽</Text>
          <Text style={styles.title}>Análisis de Apuestas</Text>
          <Text style={styles.subtitle}>Ingresa los datos del partido para obtener recomendaciones</Text>
        </View>

        <View style={styles.form}>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Nombre del Partido *</Text>
            <TextInput
              style={styles.input}
              placeholder="Ej: Real Madrid vs Barcelona"
              placeholderTextColor="#95a5a6"
              value={matchName}
              onChangeText={setMatchName}
            />
          </View>

          <Text style={styles.sectionTitle}>Cuotas 1X2 (Obligatorias)</Text>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Victoria Local *</Text>
            <TextInput
              style={styles.input}
              placeholder="Ej: 2.10"
              placeholderTextColor="#95a5a6"
              value={homeWin}
              onChangeText={setHomeWin}
              keyboardType="decimal-pad"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Empate *</Text>
            <TextInput
              style={styles.input}
              placeholder="Ej: 3.20"
              placeholderTextColor="#95a5a6"
              value={draw}
              onChangeText={setDraw}
              keyboardType="decimal-pad"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Victoria Visitante *</Text>
            <TextInput
              style={styles.input}
              placeholder="Ej: 3.50"
              placeholderTextColor="#95a5a6"
              value={awayWin}
              onChangeText={setAwayWin}
              keyboardType="decimal-pad"
            />
          </View>

          <Text style={styles.sectionTitle}>Cuotas Adicionales (Opcionales)</Text>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Más de 2.5 goles</Text>
            <TextInput
              style={styles.input}
              placeholder="Ej: 1.85"
              placeholderTextColor="#95a5a6"
              value={over25}
              onChangeText={setOver25}
              keyboardType="decimal-pad"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Ambos equipos marcan</Text>
            <TextInput
              style={styles.input}
              placeholder="Ej: 1.70"
              placeholderTextColor="#95a5a6"
              value={bttsYes}
              onChangeText={setBttsYes}
              keyboardType="decimal-pad"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Bankroll (€) *</Text>
            <TextInput
              style={styles.input}
              placeholder="Ej: 1000"
              placeholderTextColor="#95a5a6"
              value={bankroll}
              onChangeText={setBankroll}
              keyboardType="decimal-pad"
            />
          </View>

          <TouchableOpacity
            style={[styles.button, loading && styles.buttonDisabled]}
            onPress={handleAnalyze}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.buttonText}>Analizar Partido</Text>
            )}
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
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
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
    marginTop: 16,
  },
  headerIcon: {
    fontSize: 48,
    marginBottom: 12,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#ecf0f1',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    color: '#95a5a6',
    textAlign: 'center',
  },
  form: {
    width: '100%',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#3498db',
    marginTop: 24,
    marginBottom: 16,
  },
  inputGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 14,
    color: '#ecf0f1',
    marginBottom: 8,
    fontWeight: '500',
  },
  input: {
    backgroundColor: '#1e1e1e',
    borderRadius: 8,
    padding: 16,
    fontSize: 16,
    color: '#ecf0f1',
    borderWidth: 1,
    borderColor: '#2c2c2c',
  },
  button: {
    backgroundColor: '#3498db',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 32,
    marginBottom: 20,
  },
  buttonDisabled: {
    backgroundColor: '#5a7a94',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default InputScreen;
