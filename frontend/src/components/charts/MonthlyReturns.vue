<template>
  <div
    ref="chartRef"
    class="monthly-returns-chart"
    :style="{ height: height }"
  />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

interface MonthlyReturn {
  year: number
  month: number
  return: number
}

interface Props {
  data: MonthlyReturn[]
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  height: '300px'
})

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

const initChart = () => {
  if (!chartRef.value || !props.data.length) return

  chart = echarts.init(chartRef.value)

  // Group data by year
  const years = [...new Set(props.data.map(d => d.year))].sort()
  const months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

  // Create heatmap data
  const heatmapData: [number, number, number][] = []

  for (const year of years) {
    const yearData = props.data.filter(d => d.year === year)
    const yearIndex = years.indexOf(year)

    for (const month of months) {
      const monthData = yearData.find(d => d.month === month)
      const value = monthData ? monthData.return : null
      heatmapData.push([yearIndex, month - 1, value !== null ? value : '-'])
    }
  }

  const option: echarts.EChartsOption = {
    tooltip: {
      position: 'top',
      formatter: (params: any) => {
        if (params.value[2] === '-') {
          return `${params.value[0]}年${params.value[1] + 1}月<br/>无数据`
        }
        const returnValue = (params.value[2] * 100).toFixed(2)
        const sign = params.value[2] >= 0 ? '+' : ''
        return `${params.value[0]}年${params.value[1] + 1}月<br/>收益率: ${sign}${returnValue}%`
      }
    },
    grid: {
      left: '15%',
      right: '10%',
      bottom: '15%',
      top: '10%'
    },
    xAxis: {
      type: 'category',
      data: years.map(String),
      splitArea: { show: true }
    },
    yAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
      splitArea: { show: true }
    },
    visualMap: {
      min: -0.15,
      max: 0.15,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '0%',
      inRange: {
        color: ['#ef4444', '#fca5a5', '#fce7f3', '#dcfce7', '#86efac', '#22c55e']
      },
      formatter: (value: number) => {
        return `${(value * 100).toFixed(0)}%`
      }
    },
    series: [{
      name: '月度收益',
      type: 'heatmap',
      data: heatmapData,
      label: {
        show: true,
        formatter: (params: any) => {
          if (params.value[2] === '-') return '-'
          const val = params.value[2]
          const sign = val >= 0 ? '+' : ''
          return `${sign}${(val * 100).toFixed(0)}%`
        },
        color: '#000'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }

  chart.setOption(option)
}

const resizeChart = () => {
  chart?.resize()
}

watch(() => props.data, () => {
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
.monthly-returns-chart {
  width: 100%;
}
</style>