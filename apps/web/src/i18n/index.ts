// i18n setup (ADR-0008): pt-BR default, en-US; choice persisted in localStorage.
import i18next, { type i18n as I18n } from 'i18next'
import LanguageDetector from 'i18next-browser-languagedetector'
import { initReactI18next } from 'react-i18next'

import enUS from './locales/en-US/common.json'
import ptBR from './locales/pt-BR/common.json'

export const SUPPORTED_LOCALES = ['pt-BR', 'en-US'] as const
export type Locale = (typeof SUPPORTED_LOCALES)[number]
export const DEFAULT_LOCALE: Locale = 'pt-BR'
export const LOCALE_STORAGE_KEY = 'finance.locale'

export const resources = {
  'pt-BR': ptBR,
  'en-US': enUS,
} as const satisfies Record<Locale, typeof ptBR>

/** Maps any BCP 47 tag (e.g. "en-GB", "pt") to a supported locale, or undefined. */
export function toSupportedLocale(tag: string | undefined): Locale | undefined {
  if (!tag) return undefined
  const lower = tag.toLowerCase()
  return (
    SUPPORTED_LOCALES.find((locale) => locale.toLowerCase() === lower) ??
    SUPPORTED_LOCALES.find((locale) => locale.split('-')[0] === lower.split('-')[0])
  )
}

function syncDocumentLanguage(language: string) {
  document.documentElement.lang = language
}

export async function createI18n(): Promise<I18n> {
  const instance = i18next.createInstance()
  instance.on('languageChanged', syncDocumentLanguage)
  await instance
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
      resources: Object.fromEntries(
        SUPPORTED_LOCALES.map((locale) => [locale, { common: resources[locale] }]),
      ),
      defaultNS: 'common',
      supportedLngs: [...SUPPORTED_LOCALES],
      fallbackLng: DEFAULT_LOCALE,
      interpolation: { escapeValue: false },
      detection: {
        order: ['localStorage', 'navigator'],
        lookupLocalStorage: LOCALE_STORAGE_KEY,
        caches: ['localStorage'],
        convertDetectedLanguage: (tag: string) => toSupportedLocale(tag) ?? tag,
      },
    })
  return instance
}
