<template>
  <div
    ref="chartRef"
    class="drawdown-chart"
    :style="{ height: height }"
  />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import * as echarts from 'echarts'

interface EquityPoint {
  date: string
  equity: number
}

interface Props {
  equityCurve: EquityPoint[]
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  height: '300px'
})

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

// Calculate drawdown from equity curve
const drawdownData = computed(() => {
  if (!props.equityCurve || props.equityCurve.length === 0) {
    return []
  }

  const result: { date: string; value: number }[] = []
  let maxEquity = props.equityCurve[0]?.equity || 0

  for (const point of props.equityCurve) {
    if (point.equity > maxEquity) {
      maxEquity = point.equity
    }
    const drawdown = (point.equity - maxEquity) / maxEquity
    result.push({
      date: point.date,
      value: drawdown
    })
  }

  return result
})

const initChart = () => {
  if (!chartRef.value || drawdownData.value.length === 0) return

  chart = echarts.init(chartRef.value)

  chart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const p = params[0]
        return `${p.name}<br/>回撤: ${(p.value * 100).toFixed(2)}%`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: drawdownData.value.map(d => d.date),
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: (value: number) => `${(value * 100).toFixed(0)}%`
      },
      max: 0,
      min: (value: { min: number }) => Math.min(value.min, -0.01)
    },
    series: [{
      name: '回撤',
      type: 'line',
      data: drawdownData.value.map(d => d.value),
      smooth: true,
      symbol: 'none',
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(239, 68, 68, 0.3)' },
          { offset: 1, color: 'rgba(239, 68, 68, 0.05)' }
        ])
      },
      lineStyle: {
        color: '#ef4444',
        width: 1
      },
      markArea: {
        silent: true,
        itemStyle: {
          color: 'rgba(239, 68, 68, 0.05)'
        }
      }
    }]
  })
}

const resizeChart = () => {
  chart?.resize()
}

watch(() => props.equityCurve, () => {
  initChart()
}, { deep: true })

onMounted(() => {
  initChart()
  window.addEventListener('resize', resizeChart)
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeChart)
  chart?.dispose()
})

defineExpose({
  getChart: () => chart
})
</script>

<style scoped>
.drawdown-chart {
  width: 100%;
}
</style>