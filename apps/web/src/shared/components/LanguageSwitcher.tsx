import { useId } from 'react'
import { useTranslation } from 'react-i18next'

import { SUPPORTED_LOCALES, toSupportedLocale } from '../../i18n'

export function LanguageSwitcher() {
  const { t, i18n } = useTranslation()
  const id = useId()

  return (
    <div>
      <label htmlFor={id}>{t('language.label')}</label>{' '}
      <select
        id={id}
        value={toSupportedLocale(i18n.resolvedLanguage)}
        onChange={(event) => void i18n.changeLanguage(event.target.value)}
      >
        {SUPPORTED_LOCALES.map((locale) => (
          <option key={locale} value={locale}>
            {t(`language.${locale}`)}
          </option>
        ))}
      </select>
    </div>
  )
}
