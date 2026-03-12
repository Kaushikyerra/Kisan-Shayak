import React from 'react';
import { Card } from 'react-native-paper';
import Screen from '../../components/common/Screen';

export default function MarketPricesScreen() {
  return (
    <Screen title="Mandi Bhav" subtitle="Live crop prices and trends.">
      <Card>
        <Card.Title title="Wheat" subtitle="₹2,350 / क्विंटल • +2.1%" />
      </Card>
      <Card>
        <Card.Title title="Soybean" subtitle="₹4,920 / क्विंटल • -1.3%" />
      </Card>
    </Screen>
  );
}
