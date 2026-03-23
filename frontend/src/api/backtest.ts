import { apiClient } from './client'
import type {
  BacktestRequest,
  BacktestRunResponse,
  BacktestResult,
  BacktestStatusResponse
} from '@/types/api'

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
  }
}
