import { Pressable, StyleSheet, Text, View } from 'react-native';
import { useEffect, useState } from 'react';
import { Screen } from '@/src/components/Screen';
import { AppHeader } from '@/src/components/AppHeader';
import { SettingRow } from '@/src/components/SettingRow';
import { colors } from '@/src/constants/colors';
import { useSettingsStore } from '@/src/store/settingsStore';
import { t } from '@/src/i18n';
import { getMonthlyUsage } from '@/src/services/quota';

export default function SettingsScreen() {
  const { aiAutomatic, manualInput, cloudSync, language, patch } = useSettingsStore();
  const [usage, setUsage] = useState(0);

  useEffect(() => { getMonthlyUsage().then(setUsage); }, []);

  return (
    <Screen>
      <AppHeader title={t(language, 'settings')} />
      <View style={styles.planCard}>
        <Text style={styles.badge}>{t(language, 'freePlan')}</Text>
        <Text style={styles.big}>{usage}/10 {t(language, 'used')}</Text>
        <Text style={styles.sub}>{t(language, 'upgradePrompt')}</Text>
        <View style={styles.progressTrack}><View style={[styles.progressBar, { width: `${Math.min((usage / 10) * 100, 100)}%` }]} /></View>
      </View>

      <Text style={styles.section}>HERKENNING</Text>
      <SettingRow title={t(language, 'aiAutomatic')} subtitle="GPT-4o Vision herkent inhoud" value={aiAutomatic} onValueChange={(value) => patch({ aiAutomatic: value })} />
      <SettingRow title={t(language, 'manualInput')} subtitle="Altijd zelf naam opgeven" value={manualInput} onValueChange={(value) => patch({ manualInput: value })} />

      <Text style={styles.section}>OPSLAG</Text>
      <SettingRow title={t(language, 'cloudSync')} subtitle="Google Drive / iCloud later" value={cloudSync} onValueChange={(value) => patch({ cloudSync: value })} />

      <Text style={styles.section}>ACCOUNT</Text>
      <Pressable style={styles.row} onPress={() => patch({ language: language === 'nl' ? 'en' : 'nl' })}>
        <Text style={styles.rowText}>{t(language, 'language')}</Text>
        <Text style={styles.rowRight}>{language === 'nl' ? 'Nederlands' : 'English'} ›</Text>
      </Pressable>

      <View style={styles.row}>
        <Text style={styles.rowText}>{t(language, 'privacyData')}</Text>
        <Text style={styles.rowRight}>›</Text>
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  planCard: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 18,
    padding: 16,
    marginBottom: 16
  },
  badge: { color: colors.text, backgroundColor: '#3E8FF7', alignSelf: 'flex-start', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 999, fontSize: 12, fontWeight: '700' },
  big: { color: colors.text, fontSize: 28, fontWeight: '800', marginTop: 10 },
  sub: { color: colors.textSoft, marginTop: 4 },
  progressTrack: { height: 10, borderRadius: 999, backgroundColor: '#244B79', marginTop: 12, overflow: 'hidden' },
  progressBar: { height: '100%', borderRadius: 999, backgroundColor: colors.accent },
  section: { color: colors.textSoft, fontWeight: '700', fontSize: 12, marginBottom: 10, marginTop: 8 },
  row: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    padding: 16,
    marginBottom: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  rowText: { color: colors.text, fontWeight: '700', fontSize: 16 },
  rowRight: { color: colors.textSoft }
});
