import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MetricCard from '@/components/common/MetricCard.vue'

describe('MetricCard', () => {
  it('should render label and value', () => {
    const wrapper = mount(MetricCard, {
      props: {
        label: '总收益率',
        value: '23.45%'
      }
    })

    expect(wrapper.text()).toContain('总收益率')
    expect(wrapper.text()).toContain('23.45%')
  })

  it('should apply positive class for up trend', () => {
    const wrapper = mount(MetricCard, {
      props: {
        label: '收益',
        value: '12.3%',
        trend: 'up'
      }
    })

    expect(wrapper.find('.metric-value').classes()).toContain('positive')
  })

  it('should apply negative class for down trend', () => {
    const wrapper = mount(MetricCard, {
      props: {
        label: '回撤',
        value: '-8.5%',
        trend: 'down'
      }
    })

    expect(wrapper.find('.metric-value').classes()).toContain('negative')
  })

  it('should render description when provided', () => {
    const wrapper = mount(MetricCard, {
      props: {
        label: 'Sharpe',
        value: '1.45',
        description: '风险调整后收益'
      }
    })

    expect(wrapper.text()).toContain('风险调整后收益')
  })
})
