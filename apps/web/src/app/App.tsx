import type { i18n as I18n } from 'i18next'
import { I18nextProvider, useTranslation } from 'react-i18next'

import { LanguageSwitcher } from '../shared/components/LanguageSwitcher'

function Home() {
  const { t } = useTranslation()
  return (
    <main>
      <header>
        <h1>{t('app.title')}</h1>
        <LanguageSwitcher />
      </header>
      <p>{t('app.tagline')}</p>
    </main>
  )
}

export function App({ i18n }: { i18n: I18n }) {
  return (
    <I18nextProvider i18n={i18n}>
      <Home />
    </I18nextProvider>
  )
}
