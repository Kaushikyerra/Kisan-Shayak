import React from 'react';
import { Card } from 'react-native-paper';
import Screen from '../../components/common/Screen';

export default function FieldsListScreen() {
  return (
    <Screen title="My Fields" subtitle="Track crop health, area, and tasks.">
      <Card>
        <Card.Title title="North Plot" subtitle="Wheat • 2.5 acres • Healthy" />
      </Card>
      <Card>
        <Card.Title title="East Plot" subtitle="Tomato • 1.2 acres • Needs irrigation" />
      </Card>
    </Screen>
  );
}
