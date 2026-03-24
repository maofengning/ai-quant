<template>
  <div class="backtest-result">
    <div class="page-header">
      <h1 class="page-title">
        回测结果
      </h1>
      <el-button @click="router.push('/backtest/config')">
        新建回测
      </el-button>
    </div>

    <!-- Loading State -->
    <div
      v-if="loading"
      class="loading-container"
    >
      <el-skeleton
        :rows="5"
        animated
      />
    </div>

    <!-- Error State -->
    <el-card
      v-else-if="error"
      class="error-card"
    >
      <el-result
        icon="error"
        title="加载失败"
        :sub-title="error"
      >
        <template #extra>
          <el-button
            type="primary"
            @click="fetchResult"
          >
            重试
          </el-button>
        </template>
      </el-result>
    </el-card>

    <!-- Running State -->
    <el-card
      v-else-if="result?.status === 'running'"
      class="running-card"
    >
      <el-result
        icon="info"
        title="回测进行中"
        :sub-title="`进度: ${progress}%`"
      >
        <template #extra>
          <el-progress
            :percentage="progress"
            :status="undefined"
          />
        </template>
      </el-result>
    </el-card>

    <!-- Completed State -->
    <template v-else-if="result?.status === 'completed'">
      <!-- Summary Cards -->
      <div class="stats-grid">
        <el-card class="stat-card">
          <div class="stat-label">
            总收益率
          </div>
          <div
            class="stat-value"
            :class="result.summary.total_return >= 0 ? 'positive' : 'negative'"
          >
            {{ formatPercent(result.summary.total_return) }}
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-label">
            年化收益率
          </div>
          <div
            class="stat-value"
            :class="result.summary.annual_return >= 0 ? 'positive' : 'negative'"
          >
            {{ formatPercent(result.summary.annual_return) }}
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-label">
            最大回撤
          </div>
          <div class="stat-value negative">
            {{ formatPercent(result.summary.max_drawdown) }}
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-label">
            夏普比率
          </div>
          <div class="stat-value">
            {{ result.summary.sharpe_ratio.toFixed(2) }}
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-label">
            胜率
          </div>
          <div class="stat-value">
            {{ formatPercent(result.summary.win_rate) }}
          </div>
        </el-card>
      </div>

      <!-- Equity Curve -->
      <el-card class="section-card">
        <template #header>
          <div class="section-title">
            权益曲线
          </div>
        </template>
        <div
          ref="chartRef"
          class="chart-container"
        />
      </el-card>

      <!-- Trades Table -->
      <el-card class="section-card">
        <template #header>
          <div class="section-title">
            交易记录
          </div>
        </template>
        <el-table
          :data="result.trades"
          style="width: 100%"
          max-height="400"
        >
          <el-table-column
            prop="datetime"
            label="时间"
            width="180"
          />
          <el-table-column
            prop="symbol"
            label="品种"
            width="120"
          />
          <el-table-column
            prop="side"
            label="方向"
            width="80"
          >
            <template #default="{ row }">
              <el-tag :type="row.side === 'buy' ? 'success' : 'danger'">
                {{ row.side === 'buy' ? '买入' : '卖出' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            prop="quantity"
            label="数量"
            width="100"
          />
          <el-table-column
            prop="price"
            label="价格"
            width="120"
          >
            <template #default="{ row }">
              {{ row.price.toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column
            prop="pnl"
            label="盈亏"
            width="120"
          >
            <template #default="{ row }">
              <span :class="row.pnl >= 0 ? 'positive' : 'negative'">
                {{ row.pnl >= 0 ? '+' : '' }}{{ row.pnl.toFixed(2) }}
              </span>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { backtestApi } from '@/api/backtest'
import type { BacktestResult } from '@/types/api'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref('')
const result = ref<BacktestResult | null>(null)
const progress = ref(0)
const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null
let pollTimer: ReturnType<typeof setInterval> | null = null

const backtestId = route.params.id as string

const formatPercent = (value: number) => {
  const sign = value >= 0 ? '+' : ''
  return `${sign}${(value * 100).toFixed(2)}%`
}

const fetchResult = async () => {
  loading.value = true
  error.value = ''

  try {
    result.value = await backtestApi.getResult(backtestId)

    if (result.value.status === 'running') {
      // Start polling for status
      pollTimer = setInterval(async () => {
        const status = await backtestApi.getStatus(backtestId)
        progress.value = status.progress

        if (status.status !== 'running') {
          if (pollTimer) {
            clearInterval(pollTimer)
            pollTimer = null
          }
          // Refresh result
          result.value = await backtestApi.getResult(backtestId)
        }
      }, 2000)
    } else if (result.value.status === 'failed') {
      error.value = '回测执行失败'
    } else {
      // Completed - render chart
      setTimeout(renderChart, 100)
    }
  } catch (err) {
    error.value = '获取回测结果失败'
  } finally {
    loading.value = false
  }
}

const renderChart = () => {
  if (!chartRef.value || !result.value?.equity_curve) return

  if (chart) {
    chart.dispose()
  }

  chart = echarts.init(chartRef.value)

  const data = result.value.equity_curve.map(point => ({
    date: point.date,
    value: point.equity
  }))

  chart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const p = params[0]
        return `${p.name}<br/>权益: ${p.value.toFixed(2)}`
      }
    },
    xAxis: {
      type: 'category',
      data: data.map(d => d.date),
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      scale: true
    },
    series: [{
      type: 'line',
      data: data.map(d => d.value),
      smooth: true,
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
          { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
        ])
      },
      lineStyle: {
        color: '#409eff'
      }
    }]
  })
}

onMounted(() => {
  fetchResult()
})

onUnmounted(() => {
  if (pollTimer) {
    clearInterval(pollTimer)
  }
  if (chart) {
    chart.dispose()
  }
})
</script>

<style scoped>
.backtest-result {
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.loading-container {
  padding: 40px;
}

.error-card,
.running-card {
  margin-bottom: 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  text-align: center;
  padding: 16px;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
}

.stat-value.positive {
  color: #10b981;
}

.stat-value.negative {
  color: #ef4444;
}

.section-card {
  margin-bottom: 24px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.chart-container {
  height: 400px;
  width: 100%;
}

.positive {
  color: #10b981;
}

.negative {
  color: #ef4444;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>