import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import { createRouter, createMemoryHistory } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'

describe('AppLayout', () => {
  const createTestRouter = () => {
    return createRouter({
      history: createMemoryHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } }
      ]
    })
  }

  it('renders header component', () => {
    const router = createTestRouter()
    render(AppLayout, {
      global: {
        plugins: [router]
      }
    })
    expect(screen.getByText('AI Quant Platform')).toBeInTheDocument()
  })

  it('renders sidebar component', () => {
    const router = createTestRouter()
    render(AppLayout, {
      global: {
        plugins: [router]
      }
    })
    expect(screen.getByText('仪表盘')).toBeInTheDocument()
    expect(screen.getByText('策略管理')).toBeInTheDocument()
  })

  it('renders router-view in main area', () => {
    const router = createTestRouter()
    router.push('/')
    const { container } = render(AppLayout, {
      global: {
        plugins: [router]
      }
    })
    // AppLayout uses router-view, not slots
    expect(container.querySelector('.el-main')).toBeInTheDocument()
    expect(container.querySelector('.main-content')).toBeInTheDocument()
  })

  it('uses Element Plus el-container structure', () => {
    const router = createTestRouter()
    const { container } = render(AppLayout, {
      global: {
        plugins: [router]
      }
    })
    expect(container.querySelector('.el-container')).toBeInTheDocument()
    expect(container.querySelector('.el-header')).toBeInTheDocument()
    expect(container.querySelector('.el-aside')).toBeInTheDocument()
    expect(container.querySelector('.el-main')).toBeInTheDocument()
  })
})