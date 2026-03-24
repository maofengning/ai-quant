import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import Optimizer from '@/views/Optimizer.vue'

// Mock API
vi.mock('@/api/strategy', () => ({
  strategyApi: {
    getList: vi.fn().mockResolvedValue({ strategies: [] })
  }
}))

describe('Optimizer', () => {
  it('renders page title', () => {
    render(Optimizer)
    expect(screen.getByText('参数优化')).toBeInTheDocument()
  })

  it('renders optimization config', () => {
    render(Optimizer)
    expect(screen.getByText('优化配置')).toBeInTheDocument()
    expect(screen.getByText('选择策略')).toBeInTheDocument()
  })
})