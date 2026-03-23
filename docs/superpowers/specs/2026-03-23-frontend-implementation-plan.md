# 前端实现计划 - 量化回测平台

## 1. 项目概述

基于 2026-03-21 设计文档，实现 Vue3 前端界面，提供策略编辑、回测配置、结果可视化、参数优化等功能。

**开发方式**：TDD（测试驱动开发）
**开发分支**：`feature/frontend-impl`（使用 git worktree）
**API 对接**：基于 `docs/api-contract.yaml` OpenAPI 规范，开发期使用 MSW mock

---

## 2. 技术栈

### 2.1 核心依赖

```json
{
  "name": "ai-quant-frontend",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "lint": "eslint . --ext .vue,.ts,.tsx",
    "format": "prettier --write 'src/**/*.{vue,ts,tsx,js,json,css}'"
  },
  "dependencies": {
    "vue": "^3.4.21",
    "vue-router": "^4.3.0",
    "pinia": "^2.1.7",
    "element-plus": "^2.6.2",
    "@element-plus/icons-vue": "^2.3.1",
    "echarts": "^5.5.0",
    "vue-echarts": "^6.7.0",
    "monaco-editor": "^0.47.0",
    "axios": "^1.6.8",
    "dayjs": "^1.11.10",
    "lodash-es": "^4.17.21"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.4",
    "vite": "^5.2.0",
    "typescript": "^5.4.3",
    "vue-tsc": "^2.0.6",
    "vitest": "^1.4.0",
    "@vitest/ui": "^1.4.0",
    "@vue/test-utils": "^2.4.5",
    "@testing-library/vue": "^8.0.2",
    "@testing-library/user-event": "^14.5.2",
    "jsdom": "^24.0.0",
    "msw": "^2.2.7",
    "eslint": "^8.57.0",
    "eslint-plugin-vue": "^9.23.0",
    "@typescript-eslint/eslint-plugin": "^7.3.1",
    "prettier": "^3.2.5"
  }
}
```

### 2.2 项目结构

```
frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── main.ts                # 应用入口
│   ├── App.vue                # 根组件
│   ├── router/                # 路由配置
│   │   └── index.ts
│   ├── stores/                # Pinia 状态管理
│   │   ├── index.ts
│   │   ├── backtest.ts        # 回测状态
│   │   ├── strategy.ts        # 策略状态
│   │   └── data.ts            # 数据状态
│   ├── views/                 # 页面组件
│   │   ├── Dashboard.vue      # 仪表盘
│   │   ├── StrategyList.vue   # 策略列表
│   │   ├── StrategyEditor.vue # 策略编辑器
│   │   ├── BacktestConfig.vue # 回测配置
│   │   ├── BacktestResult.vue # 回测结果
│   │   └── Optimizer.vue      # 参数优化
│   ├── components/            # 可复用组件
│   │   ├── layout/
│   │   │   ├── Header.vue
│   │   │   ├── Sidebar.vue
│   │   │   └── Footer.vue
│   │   ├── charts/            # 图表组件
│   │   │   ├── EquityCurve.vue      # 权益曲线
│   │   │   ├── DrawdownChart.vue    # 回撤图
│   │   │   ├── MonthlyReturns.vue   # 月度收益
│   │   │   └── TradeDistribution.vue # 交易分布
│   │   ├── editor/
│   │   │   └── CodeEditor.vue       # Monaco 编辑器封装
│   │   └── common/
│   │       ├── DataTable.vue        # 数据表格
│   │       ├── MetricCard.vue       # 指标卡片
│   │       └── Loading.vue          # 加载状态
│   ├── composables/           # 组合式函数
│   │   ├── useBacktest.ts     # 回测逻辑
│   │   ├── useStrategy.ts     # 策略逻辑
│   │   ├── useChart.ts        # 图表配置
│   │   └── useWebSocket.ts    # WebSocket 连接
│   ├── api/                   # API 请求封装
│   │   ├── client.ts          # Axios 客户端
│   │   ├── data.ts            # 数据接口
│   │   ├── strategy.ts        # 策略接口
│   │   ├── backtest.ts        # 回测接口
│   │   └── optimize.ts        # 优化接口
│   ├── types/                 # TypeScript 类型
│   │   ├── api.ts             # API 类型（从 OpenAPI 生成）
│   │   ├── store.ts           # Store 类型
│   │   └── chart.ts           # 图表类型
│   ├── utils/                 # 工具函数
│   │   ├── format.ts          # 格式化函数
│   │   ├── validate.ts        # 验证函数
│   │   └── calculate.ts       # 计算函数
│   ├── assets/                # 静态资源
│   │   └── styles/
│   │       ├── main.css
│   │       └── variables.css
│   └── mocks/                 # MSW Mock 数据
│       ├── browser.ts         # 浏览器环境 mock
│       ├── handlers.ts        # API mock handlers
│       └── data/              # Mock 数据
│           ├── strategies.ts
│           ├── backtest.ts
│           └── market.ts
├── tests/
│   ├── setup.ts               # 测试环境配置
│   ├── unit/                  # 单元测试
│   │   ├── components/
│   │   ├── composables/
│   │   └── utils/
│   └── integration/           # 集成测试
│       ├── views/
│       └── workflows/
├── index.html
├── vite.config.ts
├── tsconfig.json
├── vitest.config.ts
└── README.md
```

---

## 3. TDD 实现计划

### Phase 0: 项目初始化 (1天)

**目标**：搭建项目脚手架，配置开发环境

**步骤**：
1. 创建 Vite + Vue3 + TypeScript 项目
2. 配置 Vitest 测试环境
3. 配置 ESLint + Prettier
4. 安装 Element Plus 和 ECharts
5. 配置 MSW (Mock Service Worker)
6. 创建基础目录结构

**验收标准**：
- ✅ `npm run dev` 启动开发服务器
- ✅ `npm run test` 运行测试（即使没有测试）
- ✅ `npm run lint` 通过
- ✅ MSW 可以拦截 API 请求

**配置文件示例**：

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      exclude: ['node_modules/', 'tests/']
    }
  }
})
```

```typescript
// tests/setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest'
import { server } from '../src/mocks/browser'

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

---

### Phase 1: API 层与 Mock (2天)

**TDD 核心**：先定义 API 接口类型，编写 Mock，然后实现 API 客户端

#### 1.1 API 类型定义 (`types/api.ts`)

**从 OpenAPI 生成类型**：
```bash
# 使用 openapi-typescript 工具
npx openapi-typescript ../docs/api-contract.yaml -o src/types/api.ts
```

或手动定义：
```typescript
// types/api.ts
export interface BacktestRequest {
  strategy_id: string
  symbols: string[]
  start_date: string
  end_date: string
  initial_capital: number
  commission?: number
  slippage?: number
}

export interface BacktestResult {
  backtest_id: string
  status: 'running' | 'completed' | 'failed'
  summary: {
    total_return: number
    annual_return: number
    max_drawdown: number
    sharpe_ratio: number
    win_rate: number
  }
  equity_curve: EquityPoint[]
  trades: Trade[]
}

export interface Strategy {
  strategy_id: string
  name: string
  code: string
  created_at: string
  updated_at: string
}
```

#### 1.2 MSW Mock Handlers (`mocks/handlers.ts`)

**测试先行** (`tests/unit/api/backtest.test.ts`)：
```typescript
import { describe, it, expect } from 'vitest'
import { backtestApi } from '@/api/backtest'

describe('Backtest API', () => {
  it('should start backtest and return backtest_id', async () => {
    const request = {
      strategy_id: 'test_strat',
      symbols: ['000001.SZ'],
      start_date: '2023-01-01',
      end_date: '2024-01-01',
      initial_capital: 100000
    }

    const response = await backtestApi.run(request)

    expect(response.backtest_id).toBeDefined()
    expect(response.status).toBe('running')
  })

  it('should fetch backtest result', async () => {
    const backtestId = 'bt_test_001'

    const result = await backtestApi.getResult(backtestId)

    expect(result.backtest_id).toBe(backtestId)
    expect(result.status).toBe('completed')
    expect(result.summary.total_return).toBeTypeOf('number')
  })
})
```

**实现 Mock**：
```typescript
// mocks/handlers.ts
import { http, HttpResponse } from 'msw'
import { mockBacktestResult } from './data/backtest'

export const handlers = [
  // 启动回测
  http.post('/api/v1/backtest/run', async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json({
      backtest_id: `bt_${Date.now()}`,
      status: 'running'
    })
  }),

  // 获取回测结果
  http.get('/api/v1/backtest/:id/result', ({ params }) => {
    return HttpResponse.json(mockBacktestResult)
  }),

  // 获取策略列表
  http.get('/api/v1/strategies', () => {
    return HttpResponse.json({
      strategies: mockStrategies
    })
  })
]
```

#### 1.3 API 客户端 (`api/backtest.ts`)

**实现代码**：
```typescript
// api/client.ts
import axios from 'axios'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// api/backtest.ts
import { apiClient } from './client'
import type { BacktestRequest, BacktestResult } from '@/types/api'

export const backtestApi = {
  async run(request: BacktestRequest) {
    const { data } = await apiClient.post('/backtest/run', request)
    return data
  },

  async getResult(backtestId: string): Promise<BacktestResult> {
    const { data } = await apiClient.get(`/backtest/${backtestId}/result`)
    return data
  },

  async getStatus(backtestId: string) {
    const { data } = await apiClient.get(`/backtest/${backtestId}/status`)
    return data
  }
}
```

---

### Phase 2: 状态管理 (2天)

#### 2.1 回测 Store (`stores/backtest.ts`)

**测试先行** (`tests/unit/stores/backtest.test.ts`)：
```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useBacktestStore } from '@/stores/backtest'

describe('Backtest Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize with empty state', () => {
    const store = useBacktestStore()

    expect(store.backtests).toEqual([])
    expect(store.currentBacktest).toBeNull()
    expect(store.isRunning).toBe(false)
  })

  it('should run backtest and update state', async () => {
    const store = useBacktestStore()

    const config = {
      strategy_id: 'test',
      symbols: ['000001.SZ'],
      start_date: '2023-01-01',
      end_date: '2024-01-01',
      initial_capital: 100000
    }

    await store.runBacktest(config)

    expect(store.isRunning).toBe(true)
    expect(store.currentBacktest).not.toBeNull()
    expect(store.currentBacktest?.backtest_id).toBeDefined()
  })

  it('should fetch and update result', async () => {
    const store = useBacktestStore()
    const backtestId = 'bt_test_001'

    await store.fetchResult(backtestId)

    expect(store.currentBacktest?.status).toBe('completed')
    expect(store.currentBacktest?.summary).toBeDefined()
  })

  it('should compute total return percentage', () => {
    const store = useBacktestStore()
    store.currentBacktest = {
      summary: { total_return: 0.23 }
    } as any

    expect(store.totalReturnPercent).toBe('23.00%')
  })
})
```

**实现代码**：
```typescript
// stores/backtest.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { backtestApi } from '@/api/backtest'
import type { BacktestRequest, BacktestResult } from '@/types/api'

export const useBacktestStore = defineStore('backtest', () => {
  // State
  const backtests = ref<BacktestResult[]>([])
  const currentBacktest = ref<BacktestResult | null>(null)
  const isRunning = ref(false)

  // Getters
  const totalReturnPercent = computed(() => {
    if (!currentBacktest.value?.summary.total_return) return '0.00%'
    return (currentBacktest.value.summary.total_return * 100).toFixed(2) + '%'
  })

  // Actions
  async function runBacktest(config: BacktestRequest) {
    isRunning.value = true
    try {
      const result = await backtestApi.run(config)
      currentBacktest.value = result
      backtests.value.push(result)
      return result
    } catch (error) {
      console.error('Failed to run backtest:', error)
      throw error
    } finally {
      isRunning.value = false
    }
  }

  async function fetchResult(backtestId: string) {
    const result = await backtestApi.getResult(backtestId)
    currentBacktest.value = result

    // 更新列表中的结果
    const index = backtests.value.findIndex(b => b.backtest_id === backtestId)
    if (index !== -1) {
      backtests.value[index] = result
    }
  }

  return {
    backtests,
    currentBacktest,
    isRunning,
    totalReturnPercent,
    runBacktest,
    fetchResult
  }
})
```

#### 2.2 策略 Store (`stores/strategy.ts`)

**测试先行**：
```typescript
describe('Strategy Store', () => {
  it('should fetch strategies', async () => {
    const store = useStrategyStore()
    await store.fetchStrategies()

    expect(store.strategies.length).toBeGreaterThan(0)
  })

  it('should create new strategy', async () => {
    const store = useStrategyStore()

    const newStrategy = {
      name: 'Test Strategy',
      code: 'class MyStrategy(Strategy): pass'
    }

    await store.createStrategy(newStrategy)

    expect(store.strategies).toContainEqual(
      expect.objectContaining({ name: 'Test Strategy' })
    )
  })

  it('should validate strategy code syntax', () => {
    const store = useStrategyStore()

    const validCode = 'class MyStrategy(Strategy):\n    pass'
    expect(store.validateCode(validCode)).toBe(true)

    const invalidCode = 'class MyStrategy(Strategy):\npass'  // 缩进错误
    expect(store.validateCode(invalidCode)).toBe(false)
  })
})
```

**实现代码**：
```typescript
// stores/strategy.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { strategyApi } from '@/api/strategy'
import type { Strategy } from '@/types/api'

export const useStrategyStore = defineStore('strategy', () => {
  const strategies = ref<Strategy[]>([])
  const currentStrategy = ref<Strategy | null>(null)

  async function fetchStrategies() {
    const data = await strategyApi.list()
    strategies.value = data.strategies
  }

  async function createStrategy(strategy: { name: string; code: string }) {
    const created = await strategyApi.create(strategy)
    strategies.value.push(created)
    return created
  }

  function validateCode(code: string): boolean {
    // 简单的语法检查（生产环境应该调用后端验证）
    return code.includes('class') && code.includes('Strategy')
  }

  return {
    strategies,
    currentStrategy,
    fetchStrategies,
    createStrategy,
    validateCode
  }
})
```

---

### Phase 3: 工具函数与组合式函数 (2天)

#### 3.1 格式化工具 (`utils/format.ts`)

**测试先行** (`tests/unit/utils/format.test.ts`)：
```typescript
import { describe, it, expect } from 'vitest'
import { formatPercent, formatCurrency, formatDate } from '@/utils/format'

describe('Format Utils', () => {
  it('should format percentage', () => {
    expect(formatPercent(0.1234)).toBe('12.34%')
    expect(formatPercent(-0.056)).toBe('-5.60%')
    expect(formatPercent(1.5)).toBe('150.00%')
  })

  it('should format currency', () => {
    expect(formatCurrency(100000)).toBe('¥100,000.00')
    expect(formatCurrency(1234567.89)).toBe('¥1,234,567.89')
  })

  it('should format date', () => {
    expect(formatDate('2024-01-01')).toBe('2024-01-01')
    expect(formatDate('2024-01-01T09:30:00')).toBe('2024-01-01 09:30:00')
  })
})
```

**实现代码**：
```typescript
// utils/format.ts
export function formatPercent(value: number, decimals: number = 2): string {
  return (value * 100).toFixed(decimals) + '%'
}

export function formatCurrency(value: number): string {
  return '¥' + value.toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString)
  if (dateString.includes('T')) {
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  }
  return date.toLocaleDateString('zh-CN')
}
```

#### 3.2 计算工具 (`utils/calculate.ts`)

**测试先行**：
```typescript
describe('Calculate Utils', () => {
  it('should calculate max drawdown', () => {
    const equity = [100000, 110000, 105000, 95000, 100000]
    const maxDD = calculateMaxDrawdown(equity)

    expect(maxDD).toBeCloseTo(-0.136, 3)  // -13.6%
  })

  it('should calculate sharpe ratio', () => {
    const returns = [0.01, 0.02, -0.01, 0.03, 0.01]
    const sharpe = calculateSharpeRatio(returns)

    expect(sharpe).toBeGreaterThan(0)
  })

  it('should calculate win rate', () => {
    const trades = [
      { pnl: 100 },
      { pnl: -50 },
      { pnl: 200 },
      { pnl: -30 }
    ]
    const winRate = calculateWinRate(trades)

    expect(winRate).toBe(0.5)  // 50%
  })
})
```

**实现代码**：
```typescript
// utils/calculate.ts
export function calculateMaxDrawdown(equityCurve: number[]): number {
  let maxDD = 0
  let peak = equityCurve[0]

  for (const equity of equityCurve) {
    if (equity > peak) {
      peak = equity
    }
    const dd = (equity - peak) / peak
    if (dd < maxDD) {
      maxDD = dd
    }
  }

  return maxDD
}

export function calculateSharpeRatio(returns: number[], riskFreeRate = 0.03): number {
  const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length
  const variance = returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length
  const stdDev = Math.sqrt(variance)

  return (avgReturn * 252 - riskFreeRate) / (stdDev * Math.sqrt(252))
}

export function calculateWinRate(trades: Array<{ pnl: number }>): number {
  const winningTrades = trades.filter(t => t.pnl > 0).length
  return winningTrades / trades.length
}
```

#### 3.3 回测组合式函数 (`composables/useBacktest.ts`)

**测试先行** (`tests/unit/composables/useBacktest.test.ts`)：
```typescript
import { describe, it, expect } from 'vitest'
import { useBacktest } from '@/composables/useBacktest'

describe('useBacktest', () => {
  it('should run backtest with config', async () => {
    const { runBacktest, isLoading, result } = useBacktest()

    const config = {
      strategy_id: 'test',
      symbols: ['000001.SZ'],
      start_date: '2023-01-01',
      end_date: '2024-01-01',
      initial_capital: 100000
    }

    await runBacktest(config)

    expect(isLoading.value).toBe(false)
    expect(result.value).not.toBeNull()
    expect(result.value?.backtest_id).toBeDefined()
  })

  it('should poll for result until completed', async () => {
    const { pollResult, result } = useBacktest()

    await pollResult('bt_test_001')

    expect(result.value?.status).toBe('completed')
  })
})
```

**实现代码**：
```typescript
// composables/useBacktest.ts
import { ref } from 'vue'
import { useBacktestStore } from '@/stores/backtest'
import type { BacktestRequest } from '@/types/api'

export function useBacktest() {
  const store = useBacktestStore()
  const isLoading = ref(false)
  const error = ref<Error | null>(null)

  async function runBacktest(config: BacktestRequest) {
    isLoading.value = true
    error.value = null

    try {
      await store.runBacktest(config)
    } catch (e) {
      error.value = e as Error
    } finally {
      isLoading.value = false
    }
  }

  async function pollResult(backtestId: string, interval = 2000) {
    const poll = async () => {
      await store.fetchResult(backtestId)

      if (store.currentBacktest?.status === 'running') {
        setTimeout(poll, interval)
      }
    }

    await poll()
  }

  return {
    runBacktest,
    pollResult,
    isLoading,
    error,
    result: computed(() => store.currentBacktest)
  }
}
```

---

### Phase 4: 基础组件 (3天)

#### 4.1 指标卡片 (`components/common/MetricCard.vue`)

**测试先行** (`tests/unit/components/MetricCard.test.ts`)：
```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MetricCard from '@/components/common/MetricCard.vue'

describe('MetricCard', () => {
  it('should render metric label and value', () => {
    const wrapper = mount(MetricCard, {
      props: {
        label: '总收益率',
        value: '23.45%',
        trend: 'up'
      }
    })

    expect(wrapper.text()).toContain('总收益率')
    expect(wrapper.text()).toContain('23.45%')
  })

  it('should apply positive color for up trend', () => {
    const wrapper = mount(MetricCard, {
      props: {
        label: '收益',
        value: '12.3%',
        trend: 'up'
      }
    })

    expect(wrapper.find('.metric-value').classes()).toContain('positive')
  })

  it('should apply negative color for down trend', () => {
    const wrapper = mount(MetricCard, {
      props: {
        label: '回撤',
        value: '-8.5%',
        trend: 'down'
      }
    })

    expect(wrapper.find('.metric-value').classes()).toContain('negative')
  })
})
```

**实现代码**：
```vue
<!-- components/common/MetricCard.vue -->
<template>
  <el-card class="metric-card">
    <div class="metric-label">{{ label }}</div>
    <div
      class="metric-value"
      :class="[trendClass]"
    >
      {{ value }}
    </div>
    <div v-if="description" class="metric-description">
      {{ description }}
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  label: string
  value: string | number
  trend?: 'up' | 'down' | 'neutral'
  description?: string
}

const props = defineProps<Props>()

const trendClass = computed(() => {
  if (props.trend === 'up') return 'positive'
  if (props.trend === 'down') return 'negative'
  return 'neutral'
})
</script>

<style scoped>
.metric-card {
  text-align: center;
}

.metric-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin-bottom: 8px;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
}

.metric-value.positive {
  color: var(--el-color-success);
}

.metric-value.negative {
  color: var(--el-color-danger);
}

.metric-description {
  font-size: 12px;
  color: var(--el-text-color-placeholder);
}
</style>
```

#### 4.2 代码编辑器 (`components/editor/CodeEditor.vue`)

**测试先行**：
```typescript
describe('CodeEditor', () => {
  it('should initialize with default code', () => {
    const wrapper = mount(CodeEditor, {
      props: {
        modelValue: 'print("hello")',
        language: 'python'
      }
    })

    expect(wrapper.vm.code).toBe('print("hello")')
  })

  it('should emit update on code change', async () => {
    const wrapper = mount(CodeEditor, {
      props: {
        modelValue: '',
        language: 'python'
      }
    })

    await wrapper.vm.handleChange('new code')

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['new code'])
  })

  it('should validate code on blur', async () => {
    const wrapper = mount(CodeEditor, {
      props: {
        modelValue: 'invalid code',
        validate: true
      }
    })

    await wrapper.vm.handleBlur()

    expect(wrapper.emitted('validate')).toBeTruthy()
  })
})
```

**实现代码**：
```vue
<!-- components/editor/CodeEditor.vue -->
<template>
  <div class="code-editor">
    <div ref="editorContainer" class="editor-container"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as monaco from 'monaco-editor'

interface Props {
  modelValue: string
  language?: string
  readonly?: boolean
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  language: 'python',
  readonly: false,
  height: '400px'
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'validate': [isValid: boolean]
}>()

const editorContainer = ref<HTMLElement>()
let editor: monaco.editor.IStandaloneCodeEditor

onMounted(() => {
  if (!editorContainer.value) return

  editor = monaco.editor.create(editorContainer.value, {
    value: props.modelValue,
    language: props.language,
    theme: 'vs-dark',
    automaticLayout: true,
    readOnly: props.readonly,
    minimap: { enabled: false }
  })

  editor.onDidChangeModelContent(() => {
    emit('update:modelValue', editor.getValue())
  })
})

watch(() => props.modelValue, (newValue) => {
  if (editor && editor.getValue() !== newValue) {
    editor.setValue(newValue)
  }
})

function handleBlur() {
  const code = editor.getValue()
  const isValid = validatePythonSyntax(code)
  emit('validate', isValid)
}

function validatePythonSyntax(code: string): boolean {
  // 简单验证（生产环境应该调用后端）
  return code.trim().length > 0
}
</script>
```

#### 4.3 数据表格 (`components/common/DataTable.vue`)

**测试先行**：
```typescript
describe('DataTable', () => {
  it('should render table with data', () => {
    const columns = [
      { prop: 'name', label: '名称' },
      { prop: 'value', label: '数值' }
    ]
    const data = [
      { name: 'Item 1', value: 100 },
      { name: 'Item 2', value: 200 }
    ]

    const wrapper = mount(DataTable, {
      props: { columns, data }
    })

    expect(wrapper.text()).toContain('Item 1')
    expect(wrapper.text()).toContain('100')
  })

  it('should support sorting', async () => {
    const wrapper = mount(DataTable, {
      props: {
        columns: [{ prop: 'value', label: '数值', sortable: true }],
        data: [{ value: 100 }, { value: 50 }]
      }
    })

    await wrapper.find('.sort-btn').trigger('click')

    expect(wrapper.emitted('sort')).toBeTruthy()
  })
})
```

---

### Phase 5: 图表组件 (4天)

#### 5.1 权益曲线图 (`components/charts/EquityCurve.vue`)

**测试先行** (`tests/unit/components/charts/EquityCurve.test.ts`)：
```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import EquityCurve from '@/components/charts/EquityCurve.vue'

describe('EquityCurve', () => {
  it('should render chart with equity data', () => {
    const equityData = [
      { date: '2023-01-01', equity: 100000 },
      { date: '2023-01-02', equity: 102000 },
      { date: '2023-01-03', equity: 101500 }
    ]

    const wrapper = mount(EquityCurve, {
      props: { data: equityData }
    })

    expect(wrapper.find('.equity-chart').exists()).toBe(true)
  })

  it('should highlight max drawdown period', () => {
    const equityData = [
      { date: '2023-01-01', equity: 100000 },
      { date: '2023-01-02', equity: 95000 },  // 回撤开始
      { date: '2023-01-03', equity: 90000 },  // 最大回撤
      { date: '2023-01-04', equity: 92000 }
    ]

    const wrapper = mount(EquityCurve, {
      props: { data: equityData, highlightDrawdown: true }
    })

    // 验证图表配置包含回撤区域标记
    expect(wrapper.vm.chartOptions.series[1].type).toBe('line')
  })
})
```

**实现代码**：
```vue
<!-- components/charts/EquityCurve.vue -->
<template>
  <div class="equity-chart">
    <v-chart :option="chartOptions" :autoresize="true" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import VChart from 'vue-echarts'

use([LineChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

interface EquityPoint {
  date: string
  equity: number
}

interface Props {
  data: EquityPoint[]
  highlightDrawdown?: boolean
}

const props = defineProps<Props>()

const chartOptions = computed(() => {
  const dates = props.data.map(d => d.date)
  const equities = props.data.map(d => d.equity)

  return {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const point = params[0]
        return `${point.name}<br/>权益: ¥${point.value.toLocaleString()}`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: dates,
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: (value: number) => '¥' + (value / 1000).toFixed(0) + 'K'
      }
    },
    series: [
      {
        name: '权益曲线',
        type: 'line',
        data: equities,
        smooth: true,
        lineStyle: {
          width: 2,
          color: '#5470c6'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(84, 112, 198, 0.3)' },
              { offset: 1, color: 'rgba(84, 112, 198, 0.1)' }
            ]
          }
        }
      }
    ]
  }
})
</script>
```

#### 5.2 回撤图 (`components/charts/DrawdownChart.vue`)

**测试先行**：
```typescript
describe('DrawdownChart', () => {
  it('should calculate drawdown from equity curve', () => {
    const equity = [100000, 110000, 105000, 95000, 100000]

    const wrapper = mount(DrawdownChart, {
      props: { equityCurve: equity }
    })

    const drawdowns = wrapper.vm.drawdownSeries
    expect(drawdowns[3]).toBeCloseTo(-0.136, 3)  // 最大回撤点
  })

  it('should render drawdown as negative area chart', () => {
    const equity = [100000, 95000, 90000]

    const wrapper = mount(DrawdownChart, {
      props: { equityCurve: equity }
    })

    expect(wrapper.vm.chartOptions.series[0].type).toBe('line')
    expect(wrapper.vm.chartOptions.series[0].areaStyle).toBeDefined()
  })
})
```

**实现代码**：
```vue
<!-- components/charts/DrawdownChart.vue -->
<script setup lang="ts">
import { computed } from 'vue'
import { calculateDrawdownSeries } from '@/utils/calculate'

interface Props {
  equityCurve: number[]
  dates: string[]
}

const props = defineProps<Props>()

const drawdownSeries = computed(() => {
  return calculateDrawdownSeries(props.equityCurve)
})

const chartOptions = computed(() => ({
  tooltip: {
    trigger: 'axis',
    formatter: (params: any) => {
      const value = params[0].value * 100
      return `${params[0].name}<br/>回撤: ${value.toFixed(2)}%`
    }
  },
  xAxis: {
    type: 'category',
    data: props.dates
  },
  yAxis: {
    type: 'value',
    axisLabel: {
      formatter: (value: number) => (value * 100).toFixed(0) + '%'
    }
  },
  series: [
    {
      name: '回撤',
      type: 'line',
      data: drawdownSeries.value,
      areaStyle: {
        color: 'rgba(255, 99, 71, 0.2)'
      },
      lineStyle: {
        color: 'rgba(255, 99, 71, 0.8)'
      }
    }
  ]
}))
</script>
```

#### 5.3 月度收益热力图 (`components/charts/MonthlyReturns.vue`)

**测试先行**：
```typescript
describe('MonthlyReturns', () => {
  it('should aggregate daily returns into monthly', () => {
    const dailyReturns = [
      { date: '2023-01-01', return: 0.01 },
      { date: '2023-01-02', return: 0.02 },
      { date: '2023-02-01', return: -0.01 }
    ]

    const wrapper = mount(MonthlyReturns, {
      props: { dailyReturns }
    })

    const monthly = wrapper.vm.monthlyData
    expect(monthly['2023-01']).toBeCloseTo(0.03, 2)
    expect(monthly['2023-02']).toBe(-0.01)
  })
})
```

---

### Phase 6: 页面组件 (5天)

#### 6.1 策略编辑器页面 (`views/StrategyEditor.vue`)

**测试先行** (`tests/integration/views/StrategyEditor.test.ts`)：
```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import StrategyEditor from '@/views/StrategyEditor.vue'

describe('StrategyEditor', () => {
  it('should render code editor', () => {
    const wrapper = mount(StrategyEditor, {
      global: {
        plugins: [createPinia()]
      }
    })

    expect(wrapper.find('.code-editor').exists()).toBe(true)
  })

  it('should save strategy on submit', async () => {
    const wrapper = mount(StrategyEditor, {
      global: {
        plugins: [createPinia()]
      }
    })

    await wrapper.find('input[name="name"]').setValue('Test Strategy')
    await wrapper.find('.code-editor').setValue('class MyStrategy: pass')
    await wrapper.find('button[type="submit"]').trigger('click')

    // 验证 API 调用
    expect(wrapper.emitted('save')).toBeTruthy()
  })

  it('should validate code before saving', async () => {
    const wrapper = mount(StrategyEditor)

    await wrapper.find('.code-editor').setValue('invalid code')
    await wrapper.find('button[type="submit"]').trigger('click')

    expect(wrapper.find('.error-message').text()).toContain('代码格式错误')
  })
})
```

**实现代码**：
```vue
<!-- views/StrategyEditor.vue -->
<template>
  <div class="strategy-editor">
    <el-form :model="form" :rules="rules" ref="formRef">
      <el-form-item label="策略名称" prop="name">
        <el-input v-model="form.name" placeholder="输入策略名称" />
      </el-form-item>

      <el-form-item label="策略代码" prop="code">
        <CodeEditor v-model="form.code" language="python" @validate="handleValidate" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSave" :loading="saving">
          保存策略
        </el-button>
        <el-button @click="handleTest">测试运行</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useStrategyStore } from '@/stores/strategy'
import CodeEditor from '@/components/editor/CodeEditor.vue'

const store = useStrategyStore()
const formRef = ref()
const saving = ref(false)

const form = reactive({
  name: '',
  code: DEFAULT_STRATEGY_TEMPLATE
})

const rules = {
  name: [{ required: true, message: '请输入策略名称' }],
  code: [{ required: true, message: '请输入策略代码' }]
}

async function handleSave() {
  await formRef.value.validate()

  saving.value = true
  try {
    await store.createStrategy(form)
    ElMessage.success('策略保存成功')
  } catch (error) {
    ElMessage.error('保存失败: ' + error.message)
  } finally {
    saving.value = false
  }
}

function handleValidate(isValid: boolean) {
  if (!isValid) {
    ElMessage.warning('代码语法错误，请检查')
  }
}

const DEFAULT_STRATEGY_TEMPLATE = `
class MyStrategy(Strategy):
    """自定义策略"""

    def on_bar(self, bar: Bar, engine: Engine):
        # 在这里编写你的策略逻辑
        pass
`
</script>
```

#### 6.2 回测配置页面 (`views/BacktestConfig.vue`)

**测试先行**：
```typescript
describe('BacktestConfig', () => {
  it('should render configuration form', () => {
    const wrapper = mount(BacktestConfig)

    expect(wrapper.find('input[name="strategy"]').exists()).toBe(true)
    expect(wrapper.find('input[name="start_date"]').exists()).toBe(true)
    expect(wrapper.find('input[name="end_date"]').exists()).toBe(true)
  })

  it('should validate date range', async () => {
    const wrapper = mount(BacktestConfig)

    await wrapper.find('input[name="start_date"]').setValue('2024-01-01')
    await wrapper.find('input[name="end_date"]').setValue('2023-01-01')

    await wrapper.find('button[type="submit"]').trigger('click')

    expect(wrapper.find('.error-message').text()).toContain('结束日期必须晚于开始日期')
  })

  it('should start backtest on submit', async () => {
    const wrapper = mount(BacktestConfig, {
      global: {
        plugins: [createPinia()]
      }
    })

    // 填写表单
    await wrapper.find('select[name="strategy"]').setValue('test_strategy')
    await wrapper.find('input[name="symbols"]').setValue('000001.SZ')
    await wrapper.find('input[name="start_date"]').setValue('2023-01-01')
    await wrapper.find('input[name="end_date"]').setValue('2024-01-01')
    await wrapper.find('input[name="initial_capital"]').setValue('100000')

    await wrapper.find('button[type="submit"]').trigger('click')

    // 验证跳转到结果页面
    expect(wrapper.vm.$router.currentRoute.value.name).toBe('BacktestResult')
  })
})
```

**实现代码**：
```vue
<!-- views/BacktestConfig.vue -->
<template>
  <div class="backtest-config">
    <el-card>
      <template #header>
        <h2>回测配置</h2>
      </template>

      <el-form :model="config" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="选择策略" prop="strategy_id">
          <el-select v-model="config.strategy_id" placeholder="选择策略">
            <el-option
              v-for="strategy in strategies"
              :key="strategy.strategy_id"
              :label="strategy.name"
              :value="strategy.strategy_id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="交易标的" prop="symbols">
          <el-select v-model="config.symbols" multiple placeholder="选择标的">
            <el-option label="平安银行 (000001.SZ)" value="000001.SZ" />
            <el-option label="万科A (000002.SZ)" value="000002.SZ" />
            <el-option label="BTC/USDT" value="BTC/USDT" />
          </el-select>
        </el-form-item>

        <el-form-item label="回测区间" required>
          <el-col :span="11">
            <el-form-item prop="start_date">
              <el-date-picker
                v-model="config.start_date"
                type="date"
                placeholder="开始日期"
              />
            </el-form-item>
          </el-col>
          <el-col :span="2" style="text-align: center">-</el-col>
          <el-col :span="11">
            <el-form-item prop="end_date">
              <el-date-picker
                v-model="config.end_date"
                type="date"
                placeholder="结束日期"
              />
            </el-form-item>
          </el-col>
        </el-form-item>

        <el-form-item label="初始资金" prop="initial_capital">
          <el-input-number
            v-model="config.initial_capital"
            :min="10000"
            :step="10000"
          />
        </el-form-item>

        <el-form-item label="手续费率" prop="commission">
          <el-input-number
            v-model="config.commission"
            :min="0"
            :max="0.01"
            :step="0.0001"
            :precision="4"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="isRunning">
            开始回测
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBacktest } from '@/composables/useBacktest'
import { useStrategyStore } from '@/stores/strategy'

const router = useRouter()
const strategyStore = useStrategyStore()
const { runBacktest, isLoading: isRunning } = useBacktest()

const strategies = computed(() => strategyStore.strategies)

const config = reactive({
  strategy_id: '',
  symbols: [],
  start_date: '',
  end_date: '',
  initial_capital: 100000,
  commission: 0.0003
})

const rules = {
  strategy_id: [{ required: true, message: '请选择策略' }],
  symbols: [{ required: true, message: '请选择交易标的' }],
  start_date: [{ required: true, message: '请选择开始日期' }],
  end_date: [{ required: true, message: '请选择结束日期' }]
}

onMounted(async () => {
  await strategyStore.fetchStrategies()
})

async function handleSubmit() {
  await formRef.value.validate()

  await runBacktest(config)

  router.push({
    name: 'BacktestResult',
    params: { id: result.value.backtest_id }
  })
}
</script>
```

#### 6.3 回测结果页面 (`views/BacktestResult.vue`)

**测试先行**：
```typescript
describe('BacktestResult', () => {
  it('should display loading state while running', () => {
    const wrapper = mount(BacktestResult, {
      props: { backtestId: 'bt_running' }
    })

    expect(wrapper.find('.loading-spinner').exists()).toBe(true)
    expect(wrapper.text()).toContain('回测运行中')
  })

  it('should display result when completed', async () => {
    const wrapper = mount(BacktestResult, {
      props: { backtestId: 'bt_completed' }
    })

    await wrapper.vm.$nextTick()

    expect(wrapper.find('.metric-card').exists()).toBe(true)
    expect(wrapper.find('.equity-curve').exists()).toBe(true)
  })

  it('should display metrics summary', async () => {
    const wrapper = mount(BacktestResult, {
      props: { backtestId: 'bt_completed' }
    })

    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('总收益率')
    expect(wrapper.text()).toContain('最大回撤')
    expect(wrapper.text()).toContain('夏普比率')
  })
})
```

**实现代码**：
```vue
<!-- views/BacktestResult.vue -->
<template>
  <div class="backtest-result">
    <div v-if="isLoading" class="loading">
      <el-icon class="is-loading"><Loading /></el-icon>
      <p>回测运行中... {{ progress }}%</p>
    </div>

    <template v-else-if="result">
      <!-- 绩效指标概览 -->
      <el-row :gutter="16" class="metrics-row">
        <el-col :span="6">
          <MetricCard
            label="总收益率"
            :value="formatPercent(result.summary.total_return)"
            :trend="result.summary.total_return > 0 ? 'up' : 'down'"
          />
        </el-col>
        <el-col :span="6">
          <MetricCard
            label="年化收益"
            :value="formatPercent(result.summary.annual_return)"
            :trend="result.summary.annual_return > 0 ? 'up' : 'down'"
          />
        </el-col>
        <el-col :span="6">
          <MetricCard
            label="最大回撤"
            :value="formatPercent(result.summary.max_drawdown)"
            trend="down"
          />
        </el-col>
        <el-col :span="6">
          <MetricCard
            label="夏普比率"
            :value="result.summary.sharpe_ratio.toFixed(2)"
            trend="neutral"
          />
        </el-col>
      </el-row>

      <!-- 权益曲线 -->
      <el-card class="chart-card">
        <template #header>权益曲线</template>
        <EquityCurve :data="result.equity_curve" />
      </el-card>

      <!-- 回撤图 -->
      <el-card class="chart-card">
        <template #header>回撤分析</template>
        <DrawdownChart
          :equity-curve="equityCurve"
          :dates="dates"
        />
      </el-card>

      <!-- 交易记录 -->
      <el-card class="table-card">
        <template #header>交易记录</template>
        <DataTable
          :columns="tradeColumns"
          :data="result.trades"
        />
      </el-card>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useBacktest } from '@/composables/useBacktest'
import { formatPercent } from '@/utils/format'
import MetricCard from '@/components/common/MetricCard.vue'
import EquityCurve from '@/components/charts/EquityCurve.vue'
import DrawdownChart from '@/components/charts/DrawdownChart.vue'
import DataTable from '@/components/common/DataTable.vue'

const route = useRoute()
const { pollResult, result, isLoading } = useBacktest()

const progress = ref(0)

const equityCurve = computed(() =>
  result.value?.equity_curve.map(p => p.equity) || []
)

const dates = computed(() =>
  result.value?.equity_curve.map(p => p.date) || []
)

const tradeColumns = [
  { prop: 'datetime', label: '时间' },
  { prop: 'symbol', label: '标的' },
  { prop: 'side', label: '方向' },
  { prop: 'quantity', label: '数量' },
  { prop: 'price', label: '价格' },
  { prop: 'pnl', label: '盈亏' }
]

onMounted(async () => {
  const backtestId = route.params.id as string
  await pollResult(backtestId)
})
</script>
```

---

### Phase 7: 路由与导航 (1天)

#### 7.1 路由配置 (`router/index.ts`)

**测试先行** (`tests/unit/router/index.test.ts`)：
```typescript
import { describe, it, expect } from 'vitest'
import { createRouter, createMemoryHistory } from 'vue-router'
import routes from '@/router'

describe('Router', () => {
  it('should navigate to strategy editor', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes
    })

    await router.push('/strategies/new')

    expect(router.currentRoute.value.name).toBe('StrategyEditor')
  })

  it('should redirect to dashboard on root', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes
    })

    await router.push('/')

    expect(router.currentRoute.value.name).toBe('Dashboard')
  })
})
```

**实现代码**：
```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue')
  },
  {
    path: '/strategies',
    name: 'StrategyList',
    component: () => import('@/views/StrategyList.vue')
  },
  {
    path: '/strategies/new',
    name: 'StrategyEditor',
    component: () => import('@/views/StrategyEditor.vue')
  },
  {
    path: '/strategies/:id/edit',
    name: 'StrategyEditorEdit',
    component: () => import('@/views/StrategyEditor.vue')
  },
  {
    path: '/backtest/config',
    name: 'BacktestConfig',
    component: () => import('@/views/BacktestConfig.vue')
  },
  {
    path: '/backtest/:id',
    name: 'BacktestResult',
    component: () => import('@/views/BacktestResult.vue')
  },
  {
    path: '/optimize',
    name: 'Optimizer',
    component: () => import('@/views/Optimizer.vue')
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
```

---

### Phase 8: WebSocket 实时通信 (2天)

#### 8.1 WebSocket 组合式函数 (`composables/useWebSocket.ts`)

**测试先行**：
```typescript
describe('useWebSocket', () => {
  it('should connect to WebSocket server', async () => {
    const { connect, isConnected } = useWebSocket()

    await connect('ws://localhost:8000/ws/backtest/bt_001')

    expect(isConnected.value).toBe(true)
  })

  it('should receive progress messages', async () => {
    const { connect, onMessage } = useWebSocket()
    const messages = ref([])

    onMessage((msg) => {
      messages.value.push(msg)
    })

    await connect('ws://localhost:8000/ws/backtest/bt_001')

    // 模拟收到消息
    await waitFor(() => messages.value.length > 0)

    expect(messages.value[0].type).toBe('progress')
  })
})
```

**实现代码**：
```typescript
// composables/useWebSocket.ts
import { ref, onUnmounted } from 'vue'

export function useWebSocket() {
  const ws = ref<WebSocket | null>(null)
  const isConnected = ref(false)
  const messageHandlers = ref<Array<(msg: any) => void>>([])

  function connect(url: string) {
    ws.value = new WebSocket(url)

    ws.value.onopen = () => {
      isConnected.value = true
    }

    ws.value.onmessage = (event) => {
      const message = JSON.parse(event.data)
      messageHandlers.value.forEach(handler => handler(message))
    }

    ws.value.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    ws.value.onclose = () => {
      isConnected.value = false
    }
  }

  function disconnect() {
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }
  }

  function send(data: any) {
    if (ws.value && isConnected.value) {
      ws.value.send(JSON.stringify(data))
    }
  }

  function onMessage(handler: (msg: any) => void) {
    messageHandlers.value.push(handler)
  }

  onUnmounted(() => {
    disconnect()
  })

  return {
    connect,
    disconnect,
    send,
    onMessage,
    isConnected
  }
}
```

---

### Phase 9: 集成测试与优化 (2天)

#### 9.1 用户流程测试 (`tests/integration/workflows/backtest-flow.test.ts`)

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from '@/App.vue'

describe('Complete Backtest Workflow', () => {
  it('should complete full backtest flow: create strategy → configure → run → view result', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes
    })

    const wrapper = mount(App, {
      global: {
        plugins: [router, createPinia()]
      }
    })

    // 1. 导航到策略创建页面
    await router.push('/strategies/new')
    await wrapper.vm.$nextTick()

    // 2. 创建策略
    await wrapper.find('input[name="name"]').setValue('Test Strategy')
    await wrapper.find('.code-editor').setValue('class MyStrategy(Strategy): pass')
    await wrapper.find('button[type="submit"]').trigger('click')
    await wrapper.vm.$nextTick()

    // 3. 导航到回测配置页面
    await router.push('/backtest/config')
    await wrapper.vm.$nextTick()

    // 4. 配置回测参数
    await wrapper.find('select[name="strategy"]').setValue('Test Strategy')
    await wrapper.find('input[name="symbols"]').setValue('000001.SZ')
    await wrapper.find('button[type="submit"]').trigger('click')
    await wrapper.vm.$nextTick()

    // 5. 验证跳转到结果页面
    expect(router.currentRoute.value.name).toBe('BacktestResult')

    // 6. 验证结果页面显示数据
    await waitFor(() => wrapper.find('.metric-card').exists())
    expect(wrapper.find('.equity-curve').exists()).toBe(true)
  })
})
```

#### 9.2 性能优化

**组件懒加载**：
```typescript
// router/index.ts
{
  path: '/backtest/:id',
  component: () => import(/* webpackChunkName: "backtest" */ '@/views/BacktestResult.vue')
}
```

**虚拟滚动**（大数据表格）：
```vue
<template>
  <el-table-v2
    :columns="columns"
    :data="trades"
    :width="800"
    :height="600"
  />
</template>
```

---

## 4. 开发流程规范

### 4.1 TDD 红-绿-重构循环

```
🔴 RED   → 编写失败的测试
🟢 GREEN → 编写最少代码使测试通过
🔵 REFACTOR → 重构代码保持测试通过
```

### 4.2 分支管理

```bash
# 创建 worktree
cd /Users/maofengning/work/project/aicoding/ai-quant
git worktree add .claude/worktrees/frontend-impl -b feature/frontend-impl

# 开发流程
cd .claude/worktrees/frontend-impl
# 每个 Phase 完成后 commit
git add .
git commit -m "feat(phase1): implement API layer with MSW mocks"

# Phase 完成后推送
git push origin feature/frontend-impl
```

### 4.3 测试覆盖率要求

- **单元测试覆盖率**: ≥ 75%
- **组件测试覆盖率**: ≥ 80%
- **关键组件覆盖率**: ≥ 90% (图表、编辑器)

```bash
# 运行测试并生成覆盖率报告
npm run test:coverage
```

### 4.4 代码质量检查

```bash
# 代码格式化
npm run format

# 代码检查
npm run lint

# 类型检查
npm run type-check
```

---

## 5. API 契约对接

### 5.1 从 OpenAPI 生成类型

```bash
# 安装工具
npm install -D openapi-typescript

# 生成 TypeScript 类型
npx openapi-typescript ../docs/api-contract.yaml -o src/types/api.ts
```

### 5.2 MSW Mock 配置

```typescript
// main.ts
if (import.meta.env.MODE === 'development') {
  const { worker } = await import('./mocks/browser')
  await worker.start()
}
```

### 5.3 切换到真实 API

```typescript
// .env.development (使用 Mock)
VITE_API_BASE_URL=/api/v1
VITE_USE_MOCK=true

// .env.production (使用真实后端)
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_USE_MOCK=false
```

---

## 6. 时间估算

| Phase | 模块 | 工作量 | 依赖 |
|-------|------|-------|------|
| Phase 0 | 项目初始化 | 1天 | - |
| Phase 1 | API 层与 Mock | 2天 | Phase 0 |
| Phase 2 | 状态管理 | 2天 | Phase 1 |
| Phase 3 | 工具函数与组合式函数 | 2天 | Phase 2 |
| Phase 4 | 基础组件 | 3天 | Phase 3 |
| Phase 5 | 图表组件 | 4天 | Phase 4 |
| Phase 6 | 页面组件 | 5天 | Phase 4, 5 |
| Phase 7 | 路由与导航 | 1天 | Phase 6 |
| Phase 8 | WebSocket 实时通信 | 2天 | Phase 6 |
| Phase 9 | 集成测试与优化 | 2天 | 所有 Phase |

**总计**: 约 24 个工作日（1 人月）

---

## 7. 里程碑验收标准

### Milestone 1: 基础设施完成 (Phase 0-3)
- ✅ 所有单元测试通过
- ✅ MSW Mock 正常工作
- ✅ Pinia Store 状态管理正常
- ✅ 工具函数测试覆盖率 ≥ 90%

### Milestone 2: 组件库完成 (Phase 4-5)
- ✅ 所有组件测试通过
- ✅ 图表正确渲染数据
- ✅ 代码编辑器功能正常
- ✅ Storybook 文档完整（可选）

### Milestone 3: 功能完整 (Phase 6-9)
- ✅ 所有页面测试通过
- ✅ 用户流程测试通过
- ✅ WebSocket 实时更新正常
- ✅ 性能测试通过（首屏加载 < 3s）

---

## 8. 风险与对策

| 风险 | 影响 | 对策 |
|-----|------|------|
| API 契约变更 | 前端调用失败 | 使用 TypeScript 类型检查，契约变更时自动报错 |
| Monaco Editor 打包体积大 | 首屏加载慢 | 使用 CDN 加载或 Web Worker |
| ECharts 配置复杂 | 图表显示错误 | 充分的单元测试，使用 vue-echarts 封装 |
| WebSocket 连接不稳定 | 进度更新中断 | 实现自动重连机制 |

---

## 9. 后续扩展预留

### 9.1 移动端适应
- 响应式布局（Element Plus 内置）
- 移动端图表适配

### 9.2 协作功能
- 策略分享
- 多人协作编辑（OT/CRDT）

### 9.3 AI 功能
- AI 策略代码补全（集成 Copilot）
- AI 回测结果解读
- 智能参数推荐

---

## 10. 参考资料

- [Vue 3 文档](https://cn.vuejs.org/)
- [Vitest 文档](https://cn.vitest.dev/)
- [Element Plus 文档](https://element-plus.org/zh-CN/)
- [ECharts 文档](https://echarts.apache.org/zh/index.html)
- [MSW 文档](https://mswjs.io/)
- [Monaco Editor 文档](https://microsoft.github.io/monaco-editor/)
