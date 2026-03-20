import nl from './nl';
import en from './en';

export type TranslationKey = keyof typeof nl;
const dictionaries = { nl, en };

export function t(lang: 'nl' | 'en', key: TranslationKey): string {
  return dictionaries[lang][key] ?? key;
}
