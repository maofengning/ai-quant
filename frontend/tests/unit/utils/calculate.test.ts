import { describe, it, expect } from 'vitest'
import { calculateMaxDrawdown, calculateSharpeRatio, calculateWinRate } from '@/utils/calculate'

describe('Calculate Utils', () => {
  it('should calculate max drawdown', () => {
    const equity = [100000, 110000, 105000, 95000, 100000]
    const maxDD = calculateMaxDrawdown(equity)

    expect(maxDD).toBeCloseTo(-0.136, 3)  // -13.6%
  })

  it('should calculate sharpe ratio', () => {
    const returns = [0.01, 0.02, -0.01, 0.03, 0.01]
    const sharpe = calculateSharpeRatio(returns)

    expect(sharpe).toBeGreaterThan(0)
  })

  it('should calculate win rate', () => {
    const trades = [
      { pnl: 100 },
      { pnl: -50 },
      { pnl: 200 },
      { pnl: -30 }
    ]
    const winRate = calculateWinRate(trades)

    expect(winRate).toBe(0.5)  // 50%
  })
})
