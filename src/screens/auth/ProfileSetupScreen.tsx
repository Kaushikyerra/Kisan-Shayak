import React, { useState } from 'react';
import { Button, SegmentedButtons, TextInput } from 'react-native-paper';
import Screen from '../../components/common/Screen';
import { useAuthStore } from '../../store/authStore';

export default function ProfileSetupScreen() {
  const [name, setName] = useState('');
  const [language, setLanguage] = useState('hi');
  const login = useAuthStore((s) => s.login);

  return (
    <Screen title="Profile Setup" subtitle="Complete your profile to continue.">
      <TextInput label="Name" mode="outlined" value={name} onChangeText={setName} />
      <SegmentedButtons
        value={language}
        onValueChange={setLanguage}
        buttons={[
          { value: 'hi', label: 'Hindi' },
          { value: 'en', label: 'English' },
        ]}
      />
      <Button mode="contained" onPress={() => login(name || 'Farmer')}>
        Continue
      </Button>
    </Screen>
  );
}
