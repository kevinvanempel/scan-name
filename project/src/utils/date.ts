export function formatShortDate(iso: string, locale: 'nl' | 'en' = 'nl') {
  return new Date(iso).toLocaleDateString(locale === 'nl' ? 'nl-NL' : 'en-US', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });
}
