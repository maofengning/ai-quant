import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import StrategyList from '@/views/StrategyList.vue'

describe('StrategyList', () => {
  it('renders page title', () => {
    render(StrategyList)
    expect(screen.getByText('策略管理')).toBeInTheDocument()
  })

  it('renders placeholder message', () => {
    render(StrategyList)
    expect(screen.getByText(/即将推出/)).toBeInTheDocument()
  })
})