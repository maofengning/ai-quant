export function calculateMaxDrawdown(equityCurve: number[]): number {
  let maxDD = 0
  let peak = equityCurve[0]

  for (const equity of equityCurve) {
    if (equity > peak) {
      peak = equity
    }
    const dd = (equity - peak) / peak
    if (dd < maxDD) {
      maxDD = dd
    }
  }

  return maxDD
}

export function calculateSharpeRatio(returns: number[], riskFreeRate = 0.03): number {
  const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length
  const variance = returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length
  const stdDev = Math.sqrt(variance)

  return (avgReturn * 252 - riskFreeRate) / (stdDev * Math.sqrt(252))
}

export function calculateWinRate(trades: Array<{ pnl: number }>): number {
  const winningTrades = trades.filter(t => t.pnl > 0).length
  return winningTrades / trades.length
}
