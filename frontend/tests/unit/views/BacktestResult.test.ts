import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import BacktestResult from '@/views/BacktestResult.vue'

describe('BacktestResult', () => {
  it('renders page title', () => {
    render(BacktestResult)
    expect(screen.getByText('回测结果')).toBeInTheDocument()
  })

  it('renders placeholder message', () => {
    render(BacktestResult)
    expect(screen.getByText(/即将推出/)).toBeInTheDocument()
  })
})