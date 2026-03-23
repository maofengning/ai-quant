// stores/backtest.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { backtestApi } from '@/api/backtest'
import type { BacktestRequest, BacktestResult } from '@/types/api'

export const useBacktestStore = defineStore('backtest', () => {
  // State
  const backtests = ref<BacktestResult[]>([])
  const currentBacktest = ref<BacktestResult | null>(null)
  const isRunning = ref(false)

  // Getters
  const totalReturnPercent = computed(() => {
    if (!currentBacktest.value?.summary.total_return) return '0.00%'
    return (currentBacktest.value.summary.total_return * 100).toFixed(2) + '%'
  })

  // Actions
  async function runBacktest(config: BacktestRequest) {
    isRunning.value = true
    try {
      const result = await backtestApi.run(config)
      currentBacktest.value = result
      backtests.value.push(result)
      return result
    } catch (error) {
      console.error('Failed to run backtest:', error)
      throw error
    } finally {
      isRunning.value = false
    }
  }

  async function fetchResult(backtestId: string) {
    const result = await backtestApi.getResult(backtestId)
    currentBacktest.value = result

    // 更新列表中的结果
    const index = backtests.value.findIndex(b => b.backtest_id === backtestId)
    if (index !== -1) {
      backtests.value[index] = result
    }
  }

  return {
    backtests,
    currentBacktest,
    isRunning,
    totalReturnPercent,
    runBacktest,
    fetchResult
  }
})
