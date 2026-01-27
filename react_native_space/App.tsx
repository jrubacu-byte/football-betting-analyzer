import React from 'react';
import { Provider as PaperProvider, DefaultTheme } from 'react-native-paper';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import RootNavigator from './src/navigation/RootNavigator';
import ErrorBoundary from './src/components/ErrorBoundary';

const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#3498db',
    background: '#0f0f0f',
    surface: '#1e1e1e',
    text: '#ecf0f1',
    error: '#e74c3c',
  },
};

export default function App() {
  return (
    <ErrorBoundary>
      <PaperProvider theme={theme}>
        <SafeAreaProvider>
          <RootNavigator />
        </SafeAreaProvider>
      </PaperProvider>
    </ErrorBoundary>
  );
}
