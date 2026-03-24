import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import StrategyList from '@/views/StrategyList.vue'

// Mock strategy API
vi.mock('@/api/strategy', () => ({
  strategyApi: {
    getList: vi.fn().mockResolvedValue({ strategies: [] }),
    delete: vi.fn().mockResolvedValue(undefined)
  }
}))

describe('StrategyList', () => {
  it('renders page title', () => {
    render(StrategyList)
    expect(screen.getByText('策略管理')).toBeInTheDocument()
  })

  it('renders new strategy button', () => {
    render(StrategyList)
    expect(screen.getByText('新建策略')).toBeInTheDocument()
  })
})