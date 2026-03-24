import { apiClient } from './client'
import type {
  BacktestRequest,
  BacktestRunResponse,
  BacktestResult,
  BacktestStatusResponse
} from '@/types/api'

export interface BacktestHistoryItem {
  backtest_id: string
  strategy_name: string
  status: 'running' | 'completed' | 'failed'
  total_return: number
  sharpe_ratio: number
  max_drawdown: number
  created_at: string
}

export interface BacktestListResponse {
  items: BacktestHistoryItem[]
  total: number
}

export const backtestApi = {
  /**
   * Start a new backtest.
   */
  async run(request: BacktestRequest): Promise<BacktestRunResponse> {
    const { data } = await apiClient.post('/backtest/run', request)
    return data
  },

  /**
   * Get backtest result.
   */
  async getResult(backtestId: string): Promise<BacktestResult> {
    const { data } = await apiClient.get(`/backtest/${backtestId}/result`)
    return data
  },

  /**
   * Get backtest status.
   */
  async getStatus(backtestId: string): Promise<BacktestStatusResponse> {
    const { data } = await apiClient.get(`/backtest/${backtestId}/status`)
    return data
  },

  /**
   * List backtest history.
   */
  async list(params?: { limit?: number; offset?: number }): Promise<BacktestListResponse> {
    const { data } = await apiClient.get('/backtest', { params })
    return data
  }
}
