import { http, HttpResponse } from 'msw'
import { mockStrategies } from './data/strategies'
import { mockBacktestResult } from './data/backtest'

export const handlers = [
  // Get symbols
  http.get('/api/v1/data/symbols', ({ request }) => {
    const url = new URL(request.url)
    const market = url.searchParams.get('market')

    if (market === 'cn_stock') {
      return HttpResponse.json({
        market,
        symbols: ['000001.SZ', '000002.SZ', '600000.SH']
      })
    }
    return HttpResponse.json({ market, symbols: [] })
  }),

  // Get strategies
  http.get('/api/v1/strategies', () => {
    return HttpResponse.json({ strategies: mockStrategies })
  }),

  // Create strategy
  http.post('/api/v1/strategies', async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json({
      strategy_id: `strat_${Date.now()}`,
      ...body,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }, { status: 201 })
  }),

  // Run backtest
  http.post('/api/v1/backtest/run', async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json({
      backtest_id: `bt_${Date.now()}`,
      status: 'running'
    })
  }),

  // Get backtest result
  http.get('/api/v1/backtest/:id/result', ({ params }) => {
    return HttpResponse.json(mockBacktestResult)
  }),

  // Get backtest status
  http.get('/api/v1/backtest/:id/status', ({ params }) => {
    return HttpResponse.json({
      backtest_id: params.id,
      status: 'completed',
      progress: 100
    })
  })
]
