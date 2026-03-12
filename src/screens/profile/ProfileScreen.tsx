import React from 'react';
import { Button, Text } from 'react-native-paper';
import Screen from '../../components/common/Screen';
import { useAuthStore } from '../../store/authStore';

export default function ProfileScreen() {
  const { userName, logout } = useAuthStore();

  return (
    <Screen title="Profile" subtitle="Manage your account and app settings.">
      <Text variant="titleMedium">{userName}</Text>
      <Button mode="outlined" onPress={logout}>
        Logout
      </Button>
    </Screen>
  );
}
