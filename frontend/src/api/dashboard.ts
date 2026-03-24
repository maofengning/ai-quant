import { apiClient } from './client'

export interface DashboardStats {
  strategy_count: number
  running_count: number
  return_30d: number
  avg_sharpe: number
}

export interface BacktestHistoryItem {
  backtest_id: string
  strategy_name: string
  status: 'running' | 'completed' | 'failed'
  total_return: number
  sharpe_ratio: number
  max_drawdown: number
  created_at: string
}

export interface DashboardResponse {
  stats: DashboardStats
  recent_backtests: BacktestHistoryItem[]
}

export const dashboardApi = {
  /**
   * Get dashboard statistics and recent backtests.
   */
  async getDashboard(): Promise<DashboardResponse> {
    const { data } = await apiClient.get('/dashboard')
    return data
  },

  /**
   * Get dashboard stats only.
   */
  async getStats(): Promise<DashboardStats> {
    const { data } = await apiClient.get('/dashboard/stats')
    return data
  }
}