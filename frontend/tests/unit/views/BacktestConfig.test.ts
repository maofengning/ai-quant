import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import BacktestConfig from '@/views/BacktestConfig.vue'

// Mock API
vi.mock('@/api/strategy', () => ({
  strategyApi: {
    getList: vi.fn().mockResolvedValue({ strategies: [] })
  }
}))

vi.mock('@/api/dashboard', () => ({
  dashboardApi: {
    getStats: vi.fn().mockResolvedValue({
      strategy_count: 0,
      running_count: 0,
      return_30d: 0,
      avg_sharpe: 0
    })
  }
}))

describe('BacktestConfig', () => {
  it('renders page title', () => {
    render(BacktestConfig)
    expect(screen.getByText('回测配置')).toBeInTheDocument()
  })

  it('renders form fields', () => {
    render(BacktestConfig)
    expect(screen.getByText('选择策略')).toBeInTheDocument()
    expect(screen.getByText('交易品种')).toBeInTheDocument()
  })
})