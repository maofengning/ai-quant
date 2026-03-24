// stores/strategy.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { strategyApi } from '@/api/strategy'
import type { Strategy, StrategyListResponse } from '@/types/api'

export const useStrategyStore = defineStore('strategy', () => {
  // State
  const strategies = ref<Strategy[]>([])
  const currentStrategy = ref<Strategy | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const total = ref(0)
  const page = ref(1)
  const pageSize = ref(10)

  // Getters
  const hasStrategies = computed(() => strategies.value.length > 0)

  // Actions
  async function fetchStrategies(params?: { page?: number; page_size?: number }): Promise<void> {
    isLoading.value = true
    error.value = null
    try {
      const response: StrategyListResponse = await strategyApi.getList(params)
      strategies.value = response.strategies
      total.value = response.strategies.length
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch strategies'
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function fetchStrategy(id: string): Promise<Strategy> {
    isLoading.value = true
    error.value = null
    try {
      const strategy = await strategyApi.getById(id)
      currentStrategy.value = strategy
      return strategy
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch strategy'
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function createStrategy(data: { name: string; code: string; description?: string }): Promise<Strategy> {
    isLoading.value = true
    error.value = null
    try {
      const strategy = await strategyApi.create(data)
      strategies.value.unshift(strategy)
      total.value++
      return strategy
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to create strategy'
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function updateStrategy(id: string, data: Partial<Strategy>): Promise<Strategy> {
    isLoading.value = true
    error.value = null
    try {
      const strategy = await strategyApi.update(id, data)
      const index = strategies.value.findIndex(s => s.strategy_id === id)
      if (index !== -1) {
        strategies.value[index] = strategy
      }
      if (currentStrategy.value?.strategy_id === id) {
        currentStrategy.value = strategy
      }
      return strategy
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to update strategy'
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function deleteStrategy(id: string): Promise<void> {
    isLoading.value = true
    error.value = null
    try {
      await strategyApi.delete(id)
      strategies.value = strategies.value.filter(s => s.strategy_id !== id)
      total.value--
      if (currentStrategy.value?.strategy_id === id) {
        currentStrategy.value = null
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to delete strategy'
      throw e
    } finally {
      isLoading.value = false
    }
  }

  function setCurrentStrategy(strategy: Strategy | null): void {
    currentStrategy.value = strategy
  }

  function setPage(newPage: number): void {
    page.value = newPage
  }

  return {
    // State
    strategies,
    currentStrategy,
    isLoading,
    error,
    total,
    page,
    pageSize,
    // Getters
    hasStrategies,
    // Actions
    fetchStrategies,
    fetchStrategy,
    createStrategy,
    updateStrategy,
    deleteStrategy,
    setCurrentStrategy,
    setPage
  }
})