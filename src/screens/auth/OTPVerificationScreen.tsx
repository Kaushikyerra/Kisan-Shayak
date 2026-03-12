import React, { useState } from 'react';
import { Button, TextInput, Text } from 'react-native-paper';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import Screen from '../../components/common/Screen';
import { AuthStackParamList } from '../../navigation/types';

type Props = NativeStackScreenProps<AuthStackParamList, 'OTPVerification'>;

export default function OTPVerificationScreen({ route, navigation }: Props) {
  const [otp, setOtp] = useState('');

  return (
    <Screen title="Verify OTP" subtitle="Enter the 6-digit code sent to your number.">
      <Text variant="bodyMedium">{route.params.phone}</Text>
      <TextInput label="OTP" mode="outlined" value={otp} onChangeText={setOtp} keyboardType="number-pad" maxLength={6} />
      <Button mode="contained" onPress={() => navigation.navigate('ProfileSetup')} disabled={otp.length !== 6}>
        Verify OTP
      </Button>
    </Screen>
  );
}
