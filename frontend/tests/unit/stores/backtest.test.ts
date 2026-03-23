import { describe, it, expect, beforeEach, beforeAll, afterEach, afterAll } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { setupServer } from 'msw/node'
import { handlers } from '@/mocks/handlers'
import { useBacktestStore } from '@/stores/backtest'

const server = setupServer(...handlers)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('Backtest Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize with empty state', () => {
    const store = useBacktestStore()

    expect(store.backtests).toEqual([])
    expect(store.currentBacktest).toBeNull()
    expect(store.isRunning).toBe(false)
  })

  it('should run backtest and update state', async () => {
    const store = useBacktestStore()

    const config = {
      strategy_id: 'test',
      symbols: ['000001.SZ'],
      start_date: '2023-01-01',
      end_date: '2024-01-01',
      initial_capital: 100000
    }

    await store.runBacktest(config)

    expect(store.isRunning).toBe(false)
    expect(store.currentBacktest).not.toBeNull()
    expect(store.currentBacktest?.backtest_id).toBeDefined()
  })

  it('should fetch and update result', async () => {
    const store = useBacktestStore()
    const backtestId = 'bt_test_001'

    await store.fetchResult(backtestId)

    expect(store.currentBacktest?.status).toBe('completed')
    expect(store.currentBacktest?.summary).toBeDefined()
  })

  it('should compute total return percentage', () => {
    const store = useBacktestStore()
    store.currentBacktest = {
      summary: { total_return: 0.23 }
    } as any

    expect(store.totalReturnPercent).toBe('23.00%')
  })
})
