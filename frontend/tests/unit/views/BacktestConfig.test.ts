import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import BacktestConfig from '@/views/BacktestConfig.vue'

describe('BacktestConfig', () => {
  it('renders page title', () => {
    render(BacktestConfig)
    expect(screen.getByText('回测配置')).toBeInTheDocument()
  })

  it('renders placeholder message', () => {
    render(BacktestConfig)
    expect(screen.getByText(/即将推出/)).toBeInTheDocument()
  })
})