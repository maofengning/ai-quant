<template>
  <div class="backtest-config">
    <div class="page-header">
      <h1 class="page-title">
        回测配置
      </h1>
    </div>

    <el-card>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="backtest-form"
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
          prop="symbols"
        >
          <el-select
            v-model="form.symbols"
            multiple
            placeholder="请选择交易品种"
            style="width: 100%"
            filterable
            allow-create
            default-first-option
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

        <el-form-item
          label="初始资金"
          prop="initial_capital"
        >
          <el-input-number
            v-model="form.initial_capital"
            :min="10000"
            :step="10000"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item
          label="手续费率"
        >
          <el-input-number
            v-model="form.commission"
            :min="0"
            :max="0.1"
            :precision="4"
            :step="0.0001"
            style="width: 100%"
          />
          <div class="form-tip">
            默认为 0.0003 (万三)
          </div>
        </el-form-item>

        <el-form-item
          label="滑点"
        >
          <el-input-number
            v-model="form.slippage"
            :min="0"
            :max="0.1"
            :precision="4"
            :step="0.0001"
            style="width: 100%"
          />
          <div class="form-tip">
            默认为 0.001 (千一)
          </div>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="running"
            size="large"
            @click="handleSubmit"
          >
            {{ running ? '回测中...' : '开始回测' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { backtestApi } from '@/api/backtest'
import { strategyApi } from '@/api/strategy'
import type { Strategy } from '@/types/api'

const router = useRouter()
const formRef = ref<FormInstance>()

const loading = ref(false)
const running = ref(false)
const strategies = ref<Strategy[]>([])

const availableSymbols = [
  '000001.SZ',
  '000300.SZ',
  '600000.SH',
  '600519.SH',
  'BTC/USDT',
  'ETH/USDT',
  'SOL/USDT'
]

const form = reactive({
  strategy_id: '',
  symbols: [] as string[],
  dateRange: ['', ''] as [string, string],
  initial_capital: 100000,
  commission: 0.0003,
  slippage: 0.001
})

const rules: FormRules = {
  strategy_id: [
    { required: true, message: '请选择策略', trigger: 'change' }
  ],
  symbols: [
    { required: true, message: '请选择至少一个交易品种', trigger: 'change' }
  ],
  dateRange: [
    { required: true, message: '请选择时间范围', trigger: 'change' }
  ],
  initial_capital: [
    { required: true, message: '请输入初始资金', trigger: 'blur' }
  ]
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

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    running.value = true
    try {
      const [start_date, end_date] = form.dateRange
      const response = await backtestApi.run({
        strategy_id: form.strategy_id,
        symbols: form.symbols,
        start_date,
        end_date,
        initial_capital: form.initial_capital,
        commission: form.commission,
        slippage: form.slippage
      })
      ElMessage.success('回测已启动')
      router.push(`/backtest/${response.backtest_id}`)
    } catch (error) {
      ElMessage.error('启动回测失败')
    } finally {
      running.value = false
    }
  })
}

onMounted(() => {
  fetchStrategies()
})
</script>

<style scoped>
.backtest-config {
  width: 100%;
  max-width: 800px;
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

.backtest-form {
  padding: 20px 0;
}

.form-tip {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}
</style>