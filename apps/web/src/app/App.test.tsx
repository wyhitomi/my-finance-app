// Scenarios from openspec spec `localization` (Web UI is localized).
import { cleanup, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it } from 'vitest'

import { createI18n } from '../i18n'
import { App } from './App'

function setBrowserLanguage(language: string) {
  Object.defineProperty(window.navigator, 'language', { value: language, configurable: true })
  Object.defineProperty(window.navigator, 'languages', { value: [language], configurable: true })
}

describe('App localization', () => {
  beforeEach(() => setBrowserLanguage('fr-FR'))

  it('defaults to Portuguese when the browser language is unsupported', async () => {
    render(<App i18n={await createI18n()} />)

    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Minhas Finanças')
    expect(document.documentElement.lang).toBe('pt-BR')
  })

  it('uses the browser language when supported', async () => {
    setBrowserLanguage('en-GB')

    render(<App i18n={await createI18n()} />)

    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('My Finances')
  })

  it('switches to English and remembers the choice', async () => {
    const user = userEvent.setup()
    render(<App i18n={await createI18n()} />)

    await user.selectOptions(screen.getByLabelText('Idioma'), 'en-US')

    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('My Finances')
    expect(document.documentElement.lang).toBe('en-US')
    expect(screen.getByLabelText('Language')).toHaveValue('en-US')

    cleanup()
    setBrowserLanguage('fr-FR')
    render(<App i18n={await createI18n()} />)
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('My Finances')
  })
})
