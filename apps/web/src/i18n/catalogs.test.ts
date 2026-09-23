import { describe, expect, it } from 'vitest'

import { resources, SUPPORTED_LOCALES } from '.'

function flattenKeys(value: unknown, prefix = ''): string[] {
  if (typeof value !== 'object' || value === null) return [prefix]
  return Object.entries(value).flatMap(([key, child]) =>
    flattenKeys(child, prefix ? `${prefix}.${key}` : key),
  )
}

describe('translation catalogs', () => {
  it('have exactly the same keys in every locale', () => {
    const [reference, ...others] = SUPPORTED_LOCALES.map((locale) =>
      flattenKeys(resources[locale]).sort(),
    )
    for (const keys of others) expect(keys).toEqual(reference)
  })

  it('have no empty translations', () => {
    for (const locale of SUPPORTED_LOCALES) {
      const values = JSON.stringify(resources[locale])
      expect(values).not.toContain('""')
    }
  })
})
