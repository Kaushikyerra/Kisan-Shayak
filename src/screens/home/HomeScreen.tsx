import React from 'react';
import { Card, Text } from 'react-native-paper';
import Screen from '../../components/common/Screen';
import { useAuthStore } from '../../store/authStore';

export default function HomeScreen() {
  const userName = useAuthStore((s) => s.userName);

  return (
    <Screen title={`नमस्ते, ${userName}`} subtitle="किसान का डिजिटल साथी">
      <Card>
        <Card.Title title="Weather" subtitle="28°C, Clear Sky" />
      </Card>
      <Card>
        <Card.Title title="Quick Actions" subtitle="Market Prices • Crop Advisory • Disease Detection" />
      </Card>
      <Text variant="bodyMedium">Krishi AI is ready to help with crop advice and market intelligence.</Text>
    </Screen>
  );
}
