<template>
  <div
    ref="chartRef"
    class="equity-curve-chart"
    :style="{ height: height }"
  />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

interface EquityPoint {
  date: string
  equity: number
}

interface Props {
  data: EquityPoint[]
  baseline?: EquityPoint[]
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  height: '400px'
})

const emit = defineEmits<{
  'click': [point: EquityPoint]
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

const initChart = () => {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value)

  const data = props.data.map(point => ({
    date: point.date,
    value: point.equity
  }))

  const series: echarts.SeriesOption[] = [
    {
      name: '策略权益',
      type: 'line',
      data: data.map(d => d.value),
      smooth: true,
      symbol: 'none',
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
          { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
        ])
      },
      lineStyle: {
        color: '#409eff',
        width: 2
      }
    }
  ]

  // Add baseline if provided
  if (props.baseline && props.baseline.length > 0) {
    series.push({
      name: '基准权益',
      type: 'line',
      data: props.baseline.map(d => d.equity),
      smooth: true,
      symbol: 'none',
      lineStyle: {
        color: '#909399',
        width: 1,
        type: 'dashed'
      }
    })
  }

  chart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        let result = params[0].name + '<br/>'
        params.forEach((p: any) => {
          result += `${p.marker} ${p.seriesName}: ${p.value?.toFixed(2) || '--'}<br/>`
        })
        return result
      }
    },
    legend: {
      data: props.baseline ? ['策略权益', '基准权益'] : ['策略权益'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: props.data.map(d => d.date),
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      scale: true,
      axisLabel: {
        formatter: (value: number) => value.toLocaleString()
      }
    },
    series
  })

  // Add click handler
  chart.on('click', (params) => {
    const index = params.dataIndex
    if (index >= 0 && index < props.data.length) {
      emit('click', props.data[index])
    }
  })
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
.equity-curve-chart {
  width: 100%;
}
</style>