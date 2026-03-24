<template>
  <div class="dashboard">
    <div class="page-header">
      <h1 class="page-title">
        工作台
      </h1>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-icon">
          📊
        </div>
        <div class="stat-label">
          策略总数
        </div>
        <div class="stat-value">
          {{ stats.totalStrategies }}
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon">
          ⚡
        </div>
        <div class="stat-label">
          运行中
        </div>
        <div class="stat-value">
          {{ stats.running }}
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon">
          ✅
        </div>
        <div class="stat-label">
          近30天收益
        </div>
        <div class="stat-value">
          {{ stats.return30d }}
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon">
          📈
        </div>
        <div class="stat-label">
          夏普比率
        </div>
        <div class="stat-value">
          {{ stats.sharpeRatio }}
        </div>
      </el-card>
    </div>

    <!-- Quick Actions -->
    <el-card class="section-card">
      <template #header>
        <div class="section-title">
          快速操作
        </div>
      </template>
      <div class="quick-actions">
        <el-button
          type="primary"
          size="large"
        >
          📝 新建策略
        </el-button>
        <el-button
          type="success"
          size="large"
        >
          ⚡ 快速回测
        </el-button>
        <el-button
          type="info"
          size="large"
        >
          📊 查看报告
        </el-button>
      </div>
    </el-card>

    <!-- Recent Backtests -->
    <el-card class="section-card">
      <template #header>
        <div class="section-title">
          最近回测
        </div>
      </template>
      <el-table
        :data="recentBacktests"
        style="width: 100%"
      >
        <el-table-column
          prop="backtest_id"
          label="回测ID"
          width="120"
        />
        <el-table-column
          prop="strategy_name"
          label="策略名称"
          width="150"
        />
        <el-table-column
          prop="return"
          label="收益率"
          width="120"
        />
        <el-table-column
          prop="sharpe"
          label="夏普"
          width="100"
        />
        <el-table-column
          prop="drawdown"
          label="回撤"
          width="120"
        />
        <el-table-column
          prop="created_at"
          label="时间"
          width="150"
        />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface DashboardStats {
  totalStrategies: string
  running: string
  return30d: string
  sharpeRatio: string
}

interface RecentBacktest {
  backtest_id: string
  strategy_name: string
  return: string
  sharpe: string
  drawdown: string
  created_at: string
}

const stats = ref<DashboardStats>({
  totalStrategies: '--',
  running: '--',
  return30d: '--',
  sharpeRatio: '--'
})

const recentBacktests = ref<RecentBacktest[]>([])

// TODO: Fetch real data from API in future task
</script>

<style scoped>
.dashboard {
  width: 100%;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  text-align: center;
  padding: 20px;
}

.stat-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #111827;
}

.section-card {
  margin-bottom: 24px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.quick-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
</style>