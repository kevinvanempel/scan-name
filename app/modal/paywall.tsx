import { StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Screen } from '../../src/components/Screen';
import { PrimaryButton } from '../../src/components/PrimaryButton';
import { colors } from '../../src/constants/colors';
import { useSettingsStore } from '../../src/store/settingsStore';
import { t } from '../../src/i18n';

export default function PaywallModal() {
  const language = useSettingsStore((s) => s.language);

  return (
    <Screen>
      <View style={styles.card}>
        <Text style={styles.title}>{t(language, 'monthlyLimitReached')}</Text>
        <Text style={styles.sub}>Upgrade later met RevenueCat of native store subscriptions.</Text>
        <View style={styles.feature}><Text style={styles.featureText}>• Onbeperkt verwerken</Text></View>
        <View style={styles.feature}><Text style={styles.featureText}>• Toegang tot batch-verwerking</Text></View>
        <View style={styles.feature}><Text style={styles.featureText}>• Toekomstige cloud sync</Text></View>
        <PrimaryButton label={t(language, 'cancel')} onPress={() => router.back()} />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 18,
    padding: 18,
    marginTop: 60
  },
  title: { color: colors.text, fontWeight: '800', fontSize: 24 },
  sub: { color: colors.textSoft, marginTop: 10, marginBottom: 16 },
  feature: { marginBottom: 8 },
  featureText: { color: colors.text, fontSize: 15 }
});
