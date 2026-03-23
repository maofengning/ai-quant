import type { BacktestResult } from '@/types/api'

export const mockBacktestResult: BacktestResult = {
  backtest_id: 'bt_test_001',
  status: 'completed',
  summary: {
    total_return: 0.23,
    annual_return: 0.18,
    max_drawdown: -0.12,
    sharpe_ratio: 1.45,
    win_rate: 0.58
  },
  equity_curve: [
    { date: '2023-01-01', equity: 100000 },
    { date: '2023-02-01', equity: 105000 },
    { date: '2023-03-01', equity: 110000 },
    { date: '2023-04-01', equity: 115000 },
    { date: '2023-05-01', equity: 123000 }
  ],
  trades: [
    {
      datetime: '2023-01-15T09:30:00',
      symbol: '000001.SZ',
      side: 'buy',
      quantity: 100,
      price: 10.0,
      pnl: 0
    },
    {
      datetime: '2023-02-20T15:00:00',
      symbol: '000001.SZ',
      side: 'sell',
      quantity: 100,
      price: 12.0,
      pnl: 200
    }
  ],
  daily_returns: []
}
