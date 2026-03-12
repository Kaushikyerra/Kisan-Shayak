import React, { useEffect } from 'react';
import { StyleSheet, View } from 'react-native';
import { Text } from 'react-native-paper';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { AuthStackParamList } from '../../navigation/types';
import { colors } from '../../theme/colors';
import { useTranslation } from 'react-i18next';

type Props = NativeStackScreenProps<AuthStackParamList, 'Splash'>;

export default function SplashScreen({ navigation }: Props) {
  const { t } = useTranslation();

  useEffect(() => {
    const timer = setTimeout(() => navigation.replace('Onboarding'), 2000);
    return () => clearTimeout(timer);
  }, [navigation]);

  return (
    <View style={styles.container}>
      <Text variant="displaySmall" style={styles.title}>{t('appName')}</Text>
      <Text variant="titleMedium" style={styles.tagline}>{t('tagline')}</Text>
      <Text variant="labelMedium" style={styles.version}>v1.0.0</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.surface },
  title: { color: colors.primary, fontWeight: '700' },
  tagline: { color: colors.textSecondary, marginTop: 12 },
  version: { position: 'absolute', bottom: 24, color: colors.textSecondary },
});
