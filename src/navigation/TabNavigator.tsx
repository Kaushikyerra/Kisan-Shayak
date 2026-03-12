import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import HomeScreen from '../screens/home/HomeScreen';
import FieldsListScreen from '../screens/fields/FieldsListScreen';
import ChatScreen from '../screens/ai/ChatScreen';
import MarketPricesScreen from '../screens/market/MarketPricesScreen';
import ProfileScreen from '../screens/profile/ProfileScreen';
import { MainTabParamList } from './types';

const Tab = createBottomTabNavigator<MainTabParamList>();

export default function TabNavigator() {
  return (
    <Tab.Navigator screenOptions={{ headerShown: false }}>
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Fields" component={FieldsListScreen} />
      <Tab.Screen name="KrishiAI" component={ChatScreen} options={{ title: 'Krishi AI' }} />
      <Tab.Screen name="Market" component={MarketPricesScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
