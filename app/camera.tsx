import { useRef, useState } from 'react';
import { Alert, Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { Screen } from '../src/components/Screen';
import { AppHeader } from '../src/components/AppHeader';
import { colors } from '../src/constants/colors';
import { analyzeMediaInCloud } from '../src/services/openaiCloud';
import { useDraftStore } from '../src/store/draftStore';
import { incrementMonthlyUsage } from '../src/services/quota';

export default function CameraScreen() {
  const cameraRef = useRef<CameraView | null>(null);
  const [permission, requestPermission] = useCameraPermissions();
  const [isBusy, setIsBusy] = useState(false);
  const setDraft = useDraftStore((s) => s.setDraft);

  async function handleTakePhoto() {
    try {
      if (!cameraRef.current || isBusy) return;
      setIsBusy(true);

      const photo = await cameraRef.current.takePictureAsync({
        quality: 0.9,
        imageType: 'jpg'
      });

      if (!photo?.uri) {
        throw new Error('Er is geen foto gemaakt.');
      }

      const suggestion = await analyzeMediaInCloud({
        uri: photo.uri,
        fileName: `camera_${Date.now()}.jpg`,
        mimeType: 'image/jpeg'
      });

      setDraft(
        {
          uri: photo.uri,
          fileName: `camera_${Date.now()}.jpg`,
          fileSize: undefined,
          mimeType: 'image/jpeg'
        },
        suggestion
      );

      await incrementMonthlyUsage();
      router.replace('/review');
    } catch (error: any) {
      Alert.alert('Fout', error?.message ?? 'Foto maken of analyseren mislukt');
    } finally {
      setIsBusy(false);
    }
  }

  if (!permission) {
    return (
      <Screen>
        <AppHeader title="Camera" subtitle="Camera rechten laden..." />
      </Screen>
    );
  }

  if (!permission.granted) {
    return (
      <Screen>
        <AppHeader title="Camera" subtitle="Toegang nodig tot je camera" />
        <Pressable style={styles.button} onPress={requestPermission}>
          <Text style={styles.buttonText}>Geef camera toegang</Text>
        </Pressable>
      </Screen>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.top}>
        <Text style={styles.title}>Maak een foto</Text>
        <Text style={styles.subtitle}>De foto wordt direct door AI geanalyseerd</Text>
      </View>

      <CameraView
        ref={cameraRef}
        style={styles.camera}
        facing="back"
        mode="picture"
      />

      <View style={styles.bottomBar}>
        <Pressable style={[styles.captureButton, isBusy && styles.captureDisabled]} onPress={handleTakePhoto}>
          <Text style={styles.captureText}>{isBusy ? 'Bezig...' : 'Foto maken'}</Text>
        </Pressable>

        <Pressable style={styles.secondaryButton} onPress={() => router.back()}>
          <Text style={styles.secondaryText}>Terug</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.bg
  },
  top: {
    paddingTop: 60,
    paddingHorizontal: 18,
    paddingBottom: 12
  },
  title: {
    color: colors.text,
    fontSize: 28,
    fontWeight: '800'
  },
  subtitle: {
    color: colors.textSoft,
    marginTop: 4
  },
  camera: {
    flex: 1,
    marginHorizontal: 18,
    borderRadius: 18,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: colors.border
  },
  bottomBar: {
    padding: 18,
    gap: 12
  },
  button: {
    backgroundColor: colors.card2,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    paddingVertical: 14,
    alignItems: 'center'
  },
  buttonText: {
    color: colors.text,
    fontWeight: '700',
    fontSize: 16
  },
  captureButton: {
    backgroundColor: colors.accent,
    borderRadius: 999,
    paddingVertical: 16,
    alignItems: 'center'
  },
  captureDisabled: {
    opacity: 0.7
  },
  captureText: {
    color: '#fff',
    fontWeight: '800',
    fontSize: 18
  },
  secondaryButton: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    paddingVertical: 14,
    alignItems: 'center'
  },
  secondaryText: {
    color: colors.text,
    fontWeight: '700'
  }
});
