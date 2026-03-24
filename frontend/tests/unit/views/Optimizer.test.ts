import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import Optimizer from '@/views/Optimizer.vue'

describe('Optimizer', () => {
  it('renders page title', () => {
    render(Optimizer)
    expect(screen.getByText('参数优化')).toBeInTheDocument()
  })

  it('renders placeholder message', () => {
    render(Optimizer)
    expect(screen.getByText(/即将推出/)).toBeInTheDocument()
  })
})