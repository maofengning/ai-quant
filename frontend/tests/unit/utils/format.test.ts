import { describe, it, expect } from 'vitest'
import { formatPercent, formatCurrency, formatDate } from '@/utils/format'

describe('Format Utils', () => {
  it('should format percentage', () => {
    expect(formatPercent(0.1234)).toBe('12.34%')
    expect(formatPercent(-0.056)).toBe('-5.60%')
    expect(formatPercent(1.5)).toBe('150.00%')
  })

  it('should format currency', () => {
    expect(formatCurrency(100000)).toBe('¥100,000.00')
    expect(formatCurrency(1234567.89)).toBe('¥1,234,567.89')
  })

  it('should format date', () => {
    expect(formatDate('2024-01-01')).toBe('2024-01-01')
    expect(formatDate('2024-01-01T09:30:00')).toBe('2024-01-01 09:30:00')
  })
})
