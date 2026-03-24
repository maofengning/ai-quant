import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/vue'
import { createPinia, setActivePinia } from 'pinia'
import Dashboard from '@/views/Dashboard.vue'

describe('Dashboard', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders page title "工作台"', () => {
    render(Dashboard)
    expect(screen.getByText('工作台')).toBeInTheDocument()
  })

  it('renders four stat cards per spec', () => {
    render(Dashboard)
    expect(screen.getByText('策略总数')).toBeInTheDocument()
    expect(screen.getByText('运行中')).toBeInTheDocument()
    expect(screen.getByText('近30天收益')).toBeInTheDocument()
    expect(screen.getByText('夏普比率')).toBeInTheDocument()
  })

  it('displays placeholder values initially', () => {
    render(Dashboard)
    const values = screen.getAllByText('--')
    expect(values.length).toBeGreaterThan(0)
  })

  it('renders quick actions section', () => {
    render(Dashboard)
    expect(screen.getByText('快速操作')).toBeInTheDocument()
  })

  it('renders recent backtest section', () => {
    render(Dashboard)
    expect(screen.getByText('最近回测')).toBeInTheDocument()
  })
})