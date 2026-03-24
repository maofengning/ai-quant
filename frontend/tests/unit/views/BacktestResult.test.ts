import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/vue'
import { createRouter, createWebHistory } from 'vue-router'
import BacktestResult from '@/views/BacktestResult.vue'

// Mock backtest API
vi.mock('@/api/backtest', () => ({
  backtestApi: {
    getStatus: vi.fn().mockResolvedValue({ backtest_id: 'test-1', status: 'completed', progress: 1.0 }),
    getResult: vi.fn().mockResolvedValue({
      backtest_id: 'test-1',
      status: 'completed',
      summary: {
        total_return: 0.15,
        annual_return: 0.25,
        max_drawdown: 0.1,
        sharpe_ratio: 1.5,
        win_rate: 0.6
      },
      equity_curve: [],
      trades: [],
      daily_returns: []
    })
  }
}))

const router = createRouter({
  history: createWebHistory('/'),
  routes: [
    { path: '/', redirect: '/backtest/result' },
    { path: '/backtest/result', name: 'backtest-result', component: {} }
  ]
})
router.push('/backtest/result?id=test-1')

describe('BacktestResult', () => {
  it('renders page title', async () => {
    render(BacktestResult, {
      global: {
        plugins: [router]
      }
    })
    expect(screen.getByText('回测结果')).toBeInTheDocument()
  })

  it('renders new backtest button', async () => {
    render(BacktestResult, {
      global: {
        plugins: [router]
      }
    })
    expect(screen.getByText('新建回测')).toBeInTheDocument()
  })
})