<template>
  <div class="optimizer">
    <div class="page-header">
      <h1 class="page-title">
        参数优化
      </h1>
    </div>

    <el-row :gutter="24">
      <!-- Config Panel -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              优化配置
            </div>
          </template>

          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            label-width="100px"
          >
            <el-form-item
              label="选择策略"
              prop="strategy_id"
            >
              <el-select
                v-model="form.strategy_id"
                placeholder="请选择策略"
                style="width: 100%"
                filterable
              >
                <el-option
                  v-for="s in strategies"
                  :key="s.strategy_id"
                  :label="s.name"
                  :value="s.strategy_id"
                />
              </el-select>
            </el-form-item>

            <el-form-item
              label="交易品种"
              prop="symbol"
            >
              <el-select
                v-model="form.symbol"
                placeholder="请选择交易品种"
                style="width: 100%"
              >
                <el-option
                  v-for="s in availableSymbols"
                  :key="s"
                  :label="s"
                  :value="s"
                />
              </el-select>
            </el-form-item>

            <el-form-item
              label="时间范围"
              prop="dateRange"
            >
              <el-date-picker
                v-model="form.dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>

            <el-divider>优化参数</el-divider>

            <div
              v-for="(param, index) in form.params"
              :key="index"
              class="param-item"
            >
              <el-form-item
                :label="`参数${index + 1}`"
                class="param-form-item"
              >
                <el-input
                  v-model="param.name"
                  placeholder="参数名"
                  style="width: 80px"
                />
              </el-form-item>
              <el-form-item label="">
                <el-input-number
                  v-model="param.start"
                  :min="0"
                  placeholder="起始"
                  style="width: 80px"
                />
                <span class="param-separator">-</span>
                <el-input-number
                  v-model="param.end"
                  :min="0"
                  placeholder="结束"
                  style="width: 80px"
                />
                <span class="param-separator">/</span>
                <el-input-number
                  v-model="param.step"
                  :min="1"
                  placeholder="步长"
                  style="width: 70px"
                />
                <el-button
                  v-if="form.params.length > 1"
                  type="danger"
                  size="small"
                  text
                  @click="removeParam(index)"
                >
                  删除
                </el-button>
              </el-form-item>
            </div>

            <el-button
              type="primary"
              text
              @click="addParam"
            >
              + 添加参数
            </el-button>

            <el-divider>优化目标</el-divider>

            <el-form-item
              label="目标指标"
              prop="objective"
            >
              <el-select
                v-model="form.objective"
                style="width: 100%"
              >
                <el-option
                  label="总收益率"
                  value="total_return"
                />
                <el-option
                  label="夏普比率"
                  value="sharpe_ratio"
                />
                <el-option
                  label="最大回撤 (越小越好)"
                  value="max_drawdown"
                />
                <el-option
                  label="胜率"
                  value="win_rate"
                />
              </el-select>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                :loading="optimizing"
                style="width: 100%"
                @click="handleOptimize"
              >
                {{ optimizing ? '优化中...' : '开始优化' }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- Results Panel -->
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              优化结果
            </div>
          </template>

          <div
            v-if="!results.length"
            class="empty-result"
          >
            <el-empty description="请配置参数并开始优化" />
          </div>

          <template v-else>
            <!-- Best Params -->
            <div class="best-params">
              <el-alert
                :title="`最佳参数: ${bestParams}`"
                :description="`${objectiveLabel}: ${bestScore}`"
                type="success"
                :closable="false"
              />
            </div>

            <!-- Results Table -->
            <el-table
              :data="results"
              style="width: 100%"
              max-height="500"
              :default-sort="{ prop: 'score', order: form.objective === 'max_drawdown' ? 'ascending' : 'descending' }"
            >
              <el-table-column
                v-for="param in form.params"
                :key="param.name"
                :prop="param.name"
                :label="param.name"
                sortable
                width="100"
              />
              <el-table-column
                prop="total_return"
                label="收益率"
                width="100"
              >
                <template #default="{ row }">
                  <span :class="row.total_return >= 0 ? 'positive' : 'negative'">
                    {{ formatPercent(row.total_return) }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                prop="sharpe_ratio"
                label="夏普"
                width="80"
              />
              <el-table-column
                prop="max_drawdown"
                label="回撤"
                width="100"
              >
                <template #default="{ row }">
                  {{ formatPercent(row.max_drawdown) }}
                </template>
              </el-table-column>
              <el-table-column
                prop="win_rate"
                label="胜率"
                width="80"
              >
                <template #default="{ row }">
                  {{ formatPercent(row.win_rate) }}
                </template>
              </el-table-column>
              <el-table-column
                prop="score"
                :label="objectiveLabel"
                sortable
                width="100"
              >
                <template #default="{ row }">
                  {{ row.score.toFixed(4) }}
                </template>
              </el-table-column>
            </el-table>
          </template>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { strategyApi } from '@/api/strategy'
import type { Strategy } from '@/types/api'

interface OptimizeParam {
  name: string
  start: number
  end: number
  step: number
}

interface OptimizeResult {
  params: Record<string, number>
  total_return: number
  sharpe_ratio: number
  max_drawdown: number
  win_rate: number
  score: number
}

const formRef = ref<FormInstance>()

const loading = ref(false)
const optimizing = ref(false)
const strategies = ref<Strategy[]>([])
const results = ref<OptimizeResult[]>([])

const availableSymbols = [
  '000001.SZ',
  '000300.SZ',
  '600000.SH',
  'BTC/USDT',
  'ETH/USDT'
]

const form = reactive({
  strategy_id: '',
  symbol: '',
  dateRange: ['', ''] as [string, string],
  params: [
    { name: 'short_window', start: 5, end: 30, step: 5 },
    { name: 'long_window', start: 20, end: 60, step: 10 }
  ] as OptimizeParam[],
  objective: 'sharpe_ratio'
})

const rules: FormRules = {
  strategy_id: [
    { required: true, message: '请选择策略', trigger: 'change' }
  ],
  symbol: [
    { required: true, message: '请选择交易品种', trigger: 'change' }
  ],
  dateRange: [
    { required: true, message: '请选择时间范围', trigger: 'change' }
  ]
}

const objectiveLabel = computed(() => {
  const labels: Record<string, string> = {
    total_return: '总收益率',
    sharpe_ratio: '夏普比率',
    max_drawdown: '最大回撤',
    win_rate: '胜率'
  }
  return labels[form.objective] || '得分'
})

const bestParams = computed(() => {
  if (!results.value.length) return ''
  const best = results.value[0]
  return Object.entries(best.params)
    .map(([k, v]) => `${k}=${v}`)
    .join(', ')
})

const bestScore = computed(() => {
  if (!results.value.length) return ''
  const best = results.value[0]
  if (form.objective === 'max_drawdown') {
    return formatPercent(best.max_drawdown)
  } else if (form.objective === 'total_return') {
    return formatPercent(best.total_return)
  } else if (form.objective === 'win_rate') {
    return formatPercent(best.win_rate)
  }
  return best.sharpe_ratio.toFixed(4)
})

const formatPercent = (value: number) => {
  const sign = value >= 0 ? '+' : ''
  return `${sign}${(value * 100).toFixed(2)}%`
}

const fetchStrategies = async () => {
  loading.value = true
  try {
    const response = await strategyApi.getList()
    strategies.value = response.strategies
  } catch (error) {
    ElMessage.error('获取策略列表失败')
  } finally {
    loading.value = false
  }
}

const addParam = () => {
  form.params.push({ name: '', start: 0, end: 0, step: 1 })
}

const removeParam = (index: number) => {
  form.params.splice(index, 1)
}

const handleOptimize = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    // Validate params
    const invalidParams = form.params.filter(
      p => !p.name || p.start >= p.end || p.step <= 0
    )
    if (invalidParams.length > 0) {
      ElMessage.error('请正确配置所有参数')
      return
    }

    optimizing.value = true
    results.value = []

    try {
      // Simulate optimization results
      // In real implementation, this would call the optimize API
      await new Promise(resolve => setTimeout(resolve, 2000))

      // Generate mock results
      const mockResults: OptimizeResult[] = []
      const param1Values = []
      const param2Values = []

      for (let p1 = form.params[0].start; p1 <= form.params[0].end; p1 += form.params[0].step) {
        param1Values.push(p1)
      }
      for (let p2 = form.params[1].start; p2 <= form.params[1].end; p2 += form.params[1].step) {
        param2Values.push(p2)
      }

      for (const p1 of param1Values) {
        for (const p2 of param2Values) {
          const total_return = (Math.random() - 0.3) * 0.5
          const sharpe_ratio = Math.random() * 2
          const max_drawdown = Math.random() * 0.3
          const win_rate = Math.random() * 0.5 + 0.3

          let score = 0
          switch (form.objective) {
            case 'total_return':
              score = total_return
              break
            case 'sharpe_ratio':
              score = sharpe_ratio
              break
            case 'max_drawdown':
              score = -max_drawdown
              break
            case 'win_rate':
              score = win_rate
              break
          }

          mockResults.push({
            params: { [form.params[0].name]: p1, [form.params[1].name]: p2 },
            total_return,
            sharpe_ratio,
            max_drawdown,
            win_rate,
            score
          })
        }
      }

      // Sort by score
      mockResults.sort((a, b) => b.score - a.score)
      results.value = mockResults

      ElMessage.success('优化完成')
    } catch (error) {
      ElMessage.error('优化失败')
    } finally {
      optimizing.value = false
    }
  })
}

onMounted(() => {
  fetchStrategies()
})
</script>

<style scoped>
.optimizer {
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

.card-header {
  font-size: 16px;
  font-weight: 600;
}

.param-item {
  margin-bottom: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 4px;
}

.param-form-item {
  margin-bottom: 8px;
}

.param-separator {
  margin: 0 4px;
  color: #909399;
}

.best-params {
  margin-bottom: 16px;
}

.empty-result {
  padding: 60px 0;
}

.positive {
  color: #10b981;
}

.negative {
  color: #ef4444;
}
</style>