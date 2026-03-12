import React from 'react';
import { Button } from 'react-native-paper';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import Screen from '../../components/common/Screen';
import { AuthStackParamList } from '../../navigation/types';

type Props = NativeStackScreenProps<AuthStackParamList, 'Onboarding'>;

export default function OnboardingScreen({ navigation }: Props) {
  return (
    <Screen title="Welcome to Kisan Sahayak" subtitle="Real-time market prices, AI crop advice, and sensor monitoring in one app.">
      <Button mode="contained" onPress={() => navigation.navigate('PhoneLogin')}>
        Get Started
      </Button>
    </Screen>
  );
}
