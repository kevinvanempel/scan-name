import { useState } from 'react';
import { Alert } from 'react-native';
import { Screen } from '../src/components/Screen';
import { AppHeader } from '../src/components/AppHeader';
import { FormField } from '../src/components/FormField';
import { PrimaryButton } from '../src/components/PrimaryButton';
import { useAuthStore } from '../src/store/authStore';

export default function AuthScreen() {
  const [email, setEmail] = useState('');
  const signIn = useAuthStore((s) => s.signIn);

  async function handleMagicLink() {
    try {
      await signIn(email);
      Alert.alert('Gelukt', 'Check je e-mail voor de magic link.');
    } catch (error: any) {
      Alert.alert('Fout', error?.message ?? 'Inloggen mislukt');
    }
  }

  return (
    <Screen>
      <AppHeader title="Inloggen" subtitle="Magic link via e-mail" />
      <FormField label="E-mail" value={email} onChangeText={setEmail} />
      <PrimaryButton label="Verstuur magic link" onPress={handleMagicLink} />
    </Screen>
  );
}
