import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import StrategyEditor from '@/views/StrategyEditor.vue'

describe('StrategyEditor', () => {
  it('renders page title', () => {
    render(StrategyEditor)
    expect(screen.getByText('策略编辑器')).toBeInTheDocument()
  })

  it('renders placeholder message', () => {
    render(StrategyEditor)
    expect(screen.getByText(/即将推出/)).toBeInTheDocument()
  })
})