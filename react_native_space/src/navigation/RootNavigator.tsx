import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Platform, Text } from 'react-native';
import InputScreen from '../screens/InputScreen';
import AnalysisScreen from '../screens/AnalysisScreen';
import HistoryScreen from '../screens/HistoryScreen';
import type { RootStackParamList, TabParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<TabParamList>();

const AnalyzeStack = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
        animation: 'slide_from_right',
      }}
    >
      <Stack.Screen name="InputScreen" component={InputScreen} />
      <Stack.Screen name="AnalysisScreen" component={AnalysisScreen} />
    </Stack.Navigator>
  );
};

const RootNavigator = () => {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={{
          headerShown: false,
          tabBarStyle: {
            backgroundColor: '#1e1e1e',
            borderTopColor: '#2c2c2c',
            borderTopWidth: 1,
            height: Platform.OS === 'ios' ? 88 : 60,
            paddingBottom: Platform.OS === 'ios' ? 24 : 8,
            paddingTop: 8,
          },
          tabBarActiveTintColor: '#3498db',
          tabBarInactiveTintColor: '#95a5a6',
          tabBarLabelStyle: {
            fontSize: 12,
            fontWeight: '600',
          },
        }}
      >
        <Tab.Screen
          name="AnalyzeTab"
          component={AnalyzeStack}
          options={{
            tabBarLabel: 'Analizar',
            tabBarIcon: ({ color }) => (
              <TabIcon icon="📊" color={color} />
            ),
          }}
        />
        <Tab.Screen
          name="HistoryScreen"
          component={HistoryScreen}
          options={{
            tabBarLabel: 'Historial',
            tabBarIcon: ({ color }) => (
              <TabIcon icon="📜" color={color} />
            ),
          }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
};

const TabIcon: React.FC<{ icon: string; color: string }> = ({ icon }) => {
  return (
    <Text style={{ fontSize: 24 }}>{icon}</Text>
  );
};

export default RootNavigator;
