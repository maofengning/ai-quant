import { describe, it, expect, beforeAll, afterEach, afterAll } from 'vitest'
import { setupServer } from 'msw/node'
import { handlers } from '@/mocks/handlers'
import { backtestApi } from '@/api/backtest'

const server = setupServer(...handlers)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('Backtest API', () => {
  it('should start backtest and return backtest_id', async () => {
    const request = {
      strategy_id: 'test_strat',
      symbols: ['000001.SZ'],
      start_date: '2023-01-01',
      end_date: '2024-01-01',
      initial_capital: 100000,
      commission: 0.0003
    }

    const response = await backtestApi.run(request)

    expect(response.backtest_id).toBeDefined()
    expect(response.status).toBe('running')
  })

  it('should fetch backtest result', async () => {
    const backtestId = 'bt_test_001'

    const result = await backtestApi.getResult(backtestId)

    expect(result.backtest_id).toBe(backtestId)
    expect(result.status).toBe('completed')
    expect(result.summary.total_return).toBeTypeOf('number')
  })
})
