import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import { App } from './app/App'
import { createI18n } from './i18n'

const root = document.getElementById('root')
if (!root) throw new Error('Missing #root element')

const i18n = await createI18n()

createRoot(root).render(
  <StrictMode>
    <App i18n={i18n} />
  </StrictMode>,
)
