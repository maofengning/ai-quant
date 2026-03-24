import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import Header from '@/components/layout/Header.vue'

describe('Header', () => {
  it('renders app title', () => {
    render(Header)
    expect(screen.getByText('AI Quant Platform')).toBeInTheDocument()
  })

  it('renders with el-header structure', () => {
    const { container } = render(Header)
    expect(container.querySelector('.el-header')).toBeInTheDocument()
  })

  it('renders header element', () => {
    const { container } = render(Header)
    const header = container.querySelector('.el-header')
    expect(header).not.toBeNull()
  })
})