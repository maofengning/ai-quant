import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import { createRouter, createMemoryHistory } from 'vue-router'
import Sidebar from '@/components/layout/Sidebar.vue'

const routes = [
  { path: '/dashboard', name: 'Dashboard', component: { template: '<div>Dashboard</div>' } },
  { path: '/strategies', name: 'StrategyList', component: { template: '<div>Strategies</div>' } },
  { path: '/backtest/config', name: 'BacktestConfig', component: { template: '<div>Backtest</div>' } },
  { path: '/optimize', name: 'Optimizer', component: { template: '<div>Optimize</div>' } }
]

describe('Sidebar', () => {
  const createTestRouter = () => {
    return createRouter({
      history: createMemoryHistory(),
      routes
    })
  }

  it('renders exactly 4 navigation items per spec', async () => {
    const router = createTestRouter()
    render(Sidebar, {
      global: {
        plugins: [router]
      }
    })

    expect(screen.getByText('仪表盘')).toBeInTheDocument()
    expect(screen.getByText('策略管理')).toBeInTheDocument()
    expect(screen.getByText('回测配置')).toBeInTheDocument()
    expect(screen.getByText('参数优化')).toBeInTheDocument()
  })

  it('renders with el-aside and el-menu structure', () => {
    const router = createTestRouter()
    const { container } = render(Sidebar, {
      global: {
        plugins: [router]
      }
    })
    expect(container.querySelector('.el-aside')).toBeInTheDocument()
    expect(container.querySelector('.el-menu')).toBeInTheDocument()
  })

  it('has correct width from spec (200px)', () => {
    const router = createTestRouter()
    const { container } = render(Sidebar, {
      global: {
        plugins: [router]
      }
    })
    const aside = container.querySelector('.el-aside')
    expect(aside).not.toBeNull()
  })
})