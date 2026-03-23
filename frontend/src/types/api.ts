export interface BacktestRequest {
  strategy_id: string
  symbols: string[]
  start_date: string
  end_date: string
  initial_capital: number
  commission?: number
  slippage?: number
}

export interface BacktestRunResponse {
  backtest_id: string
  status: 'running' | 'completed' | 'failed'
}

export interface EquityPoint {
  date: string
  equity: number
}

export interface Trade {
  datetime: string
  symbol: string
  side: 'buy' | 'sell'
  quantity: number
  price: number
  pnl: number
}

export interface BacktestSummary {
  total_return: number
  annual_return: number
  max_drawdown: number
  sharpe_ratio: number
  win_rate: number
}

export interface BacktestResult {
  backtest_id: string
  status: 'running' | 'completed' | 'failed'
  summary: BacktestSummary
  equity_curve: EquityPoint[]
  trades: Trade[]
  daily_returns: number[]
}

export interface Strategy {
  strategy_id: string
  name: string
  code: string
  created_at: string
  updated_at: string
}

export interface StrategyListResponse {
  strategies: Strategy[]
}
