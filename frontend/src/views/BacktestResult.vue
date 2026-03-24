<template>
  <div class="backtest-result">
    <div class="page-header">
      <h1 class="page-title">
        回测结果
        <span
          v-if="result?.config"
          class="backtest-info"
        >
          - {{ result.config.strategy_name }}
        </span>
      </h1>
      <div class="header-actions">
        <el-button @click="router.push('/backtest/config')">
          新建回测
        </el-button>
      </div>
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
      <!-- Tabs -->
      <el-tabs v-model="activeTab">
        <el-tab-pane
          label="概览"
          name="overview"
        >
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

          <!-- Drawdown Chart -->
          <el-card class="section-card">
            <template #header>
              <div class="section-title">
                回撤分析
              </div>
            </template>
            <div
              ref="drawdownChartRef"
              class="chart-container"
            />
          </el-card>
        </el-tab-pane>

        <el-tab-pane
          label="交易记录"
          name="trades"
        >
          <el-table
            :data="result.trades"
            style="width: 100%"
            max-height="500"
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
          <el-empty
            v-if="result.trades.length === 0"
            description="本次回测无交易记录"
          />
        </el-tab-pane>

        <el-tab-pane
          label="风险分析"
          name="risk"
        >
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card class="section-card">
                <template #header>
                  <div class="section-title">
                    月度收益
                  </div>
                </template>
                <div
                  ref="monthlyChartRef"
                  class="chart-container"
                />
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card class="section-card">
                <template #header>
                  <div class="section-title">
                    收益统计
                  </div>
                </template>
                <div class="stats-detail">
                  <div class="stat-row">
                    <span class="stat-label">交易次数</span>
                    <span class="stat-value">{{ result.trades.length }}</span>
                  </div>
                  <div class="stat-row">
                    <span class="stat-label">盈利次数</span>
                    <span class="stat-value positive">{{ profitableTrades }}</span>
                  </div>
                  <div class="stat-row">
                    <span class="stat-label">亏损次数</span>
                    <span class="stat-value negative">{{ losingTrades }}</span>
                  </div>
                  <div class="stat-row">
                    <span class="stat-label">平均盈亏</span>
                    <span :class="avgPnl >= 0 ? 'stat-value positive' : 'stat-value negative'">
                      {{ avgPnl.toFixed(2) }}
                    </span>
                  </div>
                  <div class="stat-row">
                    <span class="stat-label">最大单笔盈利</span>
                    <span class="stat-value positive">{{ maxProfit.toFixed(2) }}</span>
                  </div>
                  <div class="stat-row">
                    <span class="stat-label">最大单笔亏损</span>
                    <span class="stat-value negative">{{ maxLoss.toFixed(2) }}</span>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>

        <el-tab-pane
          label="每日收益"
          name="daily"
        >
          <el-card class="section-card">
            <template #header>
              <div class="section-title">
                每日收益分布
              </div>
            </template>
            <div
              ref="dailyChartRef"
              class="chart-container"
            />
          </el-card>
        </el-tab-pane>
      </el-tabs>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import * as echarts from 'echarts'
import { backtestApi } from '@/api/backtest'
import type { BacktestResult } from '@/types/api'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref('')
const result = ref<BacktestResult | null>(null)
const progress = ref(0)
const activeTab = ref('overview')

const chartRef = ref<HTMLElement>()
const drawdownChartRef = ref<HTMLElement>()
const monthlyChartRef = ref<HTMLElement>()
const dailyChartRef = ref<HTMLElement>()

let chart: echarts.ECharts | null = null
let drawdownChart: echarts.ECharts | null = null
let monthlyChart: echarts.ECharts | null = null
let dailyChart: echarts.ECharts | null = null

let pollTimer: ReturnType<typeof setInterval> | null = null

const backtestId = route.params.id as string

// Computed stats
const profitableTrades = computed(() => {
  return result.value?.trades.filter(t => t.pnl > 0).length || 0
})

const losingTrades = computed(() => {
  return result.value?.trades.filter(t => t.pnl < 0).length || 0
})

const avgPnl = computed(() => {
  if (!result.value?.trades.length) return 0
  const total = result.value.trades.reduce((sum, t) => sum + t.pnl, 0)
  return total / result.value.trades.length
})

const maxProfit = computed(() => {
  return Math.max(0, ...(result.value?.trades.map(t => t.pnl) || [0]))
})

const maxLoss = computed(() => {
  return Math.min(0, ...(result.value?.trades.map(t => t.pnl) || [0]))
})

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
      // Completed - render charts
      setTimeout(renderCharts, 100)
    }
  } catch (err) {
    error.value = '获取回测结果失败'
  } finally {
    loading.value = false
  }
}

const renderCharts = () => {
  renderEquityCurve()
  renderDrawdownChart()
  renderDailyReturns()
}

const renderEquityCurve = () => {
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

const renderDrawdownChart = () => {
  if (!drawdownChartRef.value || !result.value?.equity_curve) return

  if (drawdownChart) {
    drawdownChart.dispose()
  }

  drawdownChart = echarts.init(drawdownChartRef.value)

  // Calculate drawdown from equity curve
  const equityData = result.value.equity_curve
  let maxEquity = equityData[0]?.equity || 0
  const drawdowns = equityData.map(point => {
    if (point.equity > maxEquity) {
      maxEquity = point.equity
    }
    const drawdown = (point.equity - maxEquity) / maxEquity
    return {
      date: point.date,
      value: drawdown
    }
  })

  drawdownChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const p = params[0]
        return `${p.name}<br/>回撤: ${(p.value * 100).toFixed(2)}%`
      }
    },
    xAxis: {
      type: 'category',
      data: drawdowns.map(d => d.date),
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: (value: number) => `${(value * 100).toFixed(0)}%`
      }
    },
    series: [{
      type: 'line',
      data: drawdowns.map(d => d.value),
      smooth: true,
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(239, 68, 68, 0.3)' },
          { offset: 1, color: 'rgba(239, 68, 68, 0.05)' }
        ])
      },
      lineStyle: {
        color: '#ef4444'
      }
    }]
  })
}

const renderDailyReturns = () => {
  if (!dailyChartRef.value || !result.value?.daily_returns) return

  if (dailyChart) {
    dailyChart.dispose()
  }

  dailyChart = echarts.init(dailyChartRef.value)

  const data = result.value.daily_returns.map((r, i) => ({
    date: `Day ${i + 1}`,
    value: r
  }))

  dailyChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const p = params[0]
        return `${p.name}<br/>收益: ${(p.value * 100).toFixed(2)}%`
      }
    },
    xAxis: {
      type: 'category',
      data: data.map(d => d.date),
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: (value: number) => `${(value * 100).toFixed(1)}%`
      }
    },
    series: [{
      type: 'bar',
      data: data.map(d => ({
        value: d.value,
        itemStyle: {
          color: d.value >= 0 ? '#10b981' : '#ef4444'
        }
      }))
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
  if (drawdownChart) {
    drawdownChart.dispose()
  }
  if (monthlyChart) {
    monthlyChart.dispose()
  }
  if (dailyChart) {
    dailyChart.dispose()
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

.backtest-info {
  font-size: 18px;
  font-weight: 400;
  color: #6b7280;
}

.header-actions {
  display: flex;
  gap: 12px;
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

.stats-detail {
  padding: 12px 0;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.stat-row:last-child {
  border-bottom: none;
}

.stat-row .stat-label {
  color: #6b7280;
}

.stat-row .stat-value {
  font-weight: 600;
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