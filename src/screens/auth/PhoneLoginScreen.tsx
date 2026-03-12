import React, { useState } from 'react';
import { Button, TextInput } from 'react-native-paper';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import Screen from '../../components/common/Screen';
import { AuthStackParamList } from '../../navigation/types';

type Props = NativeStackScreenProps<AuthStackParamList, 'PhoneLogin'>;

export default function PhoneLoginScreen({ navigation }: Props) {
  const [phone, setPhone] = useState('');

  return (
    <Screen title="Phone Authentication" subtitle="Enter your mobile number to receive OTP.">
      <TextInput label="Phone Number" mode="outlined" value={phone} onChangeText={setPhone} keyboardType="phone-pad" />
      <Button mode="contained" onPress={() => navigation.navigate('OTPVerification', { phone })} disabled={phone.length < 10}>
        Send OTP
      </Button>
    </Screen>
  );
}
