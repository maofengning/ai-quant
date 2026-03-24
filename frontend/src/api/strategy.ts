import { apiClient } from './client'
import type { Strategy, StrategyListResponse } from '@/types/api'

export const strategyApi = {
  /**
   * Get all strategies.
   */
  async getList(): Promise<StrategyListResponse> {
    const { data } = await apiClient.get('/strategies')
    return data
  },

  /**
   * Get a single strategy by ID.
   */
  async getById(id: string): Promise<Strategy> {
    const { data } = await apiClient.get(`/strategies/${id}`)
    return data
  },

  /**
   * Create a new strategy.
   */
  async create(strategy: { name: string; code: string }): Promise<Strategy> {
    const { data } = await apiClient.post('/strategies', strategy)
    return data
  },

  /**
   * Update an existing strategy.
   */
  async update(id: string, strategy: { name?: string; code?: string }): Promise<Strategy> {
    const { data } = await apiClient.put(`/strategies/${id}`, strategy)
    return data
  },

  /**
   * Delete a strategy.
   */
  async delete(id: string): Promise<void> {
    await apiClient.delete(`/strategies/${id}`)
  }
}