import React from 'react';
import { Card, Text } from 'react-native-paper';
import Screen from '../../components/common/Screen';

export default function ChatScreen() {
  return (
    <Screen title="Krishi AI" subtitle="Ask anything about crops, weather, and prices.">
      <Card>
        <Card.Content>
          <Text variant="bodyLarge">नमस्ते! मैं कृषि AI हूँ। आज आपकी कैसे मदद कर सकता हूँ?</Text>
        </Card.Content>
      </Card>
    </Screen>
  );
}
