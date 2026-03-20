import AsyncStorage from '@react-native-async-storage/async-storage';
import { FREE_MONTHLY_LIMIT } from '@/src/constants/limits';

function usageKey() {
  const now = new Date();
  return `usage:${now.getFullYear()}-${now.getMonth() + 1}`;
}

export async function getMonthlyUsage(): Promise<number> {
  const value = await AsyncStorage.getItem(usageKey());
  return Number(value ?? '0');
}

export async function incrementMonthlyUsage(): Promise<number> {
  const current = await getMonthlyUsage();
  const next = current + 1;
  await AsyncStorage.setItem(usageKey(), String(next));
  return next;
}

export async function canProcessMore(): Promise<boolean> {
  const current = await getMonthlyUsage();
  return current < FREE_MONTHLY_LIMIT;
}
