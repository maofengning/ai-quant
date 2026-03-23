# 前端 UI 框架设计文档

## 1. 项目概述

### 1.1 目标
基于已有的后端 API 和基础前端代码，完成量化回测平台的完整 UI 框架，采用"逐层构建"方式，从 Layout → Router → Views 逐步实现。

### 1.2 当前状态
**已完成：**
- ✅ 项目脚手架（Vite + Vue3 + TypeScript）
- ✅ API 层（client.ts, backtest.ts, types/api.ts）
- ✅ MSW Mock handlers
- ✅ Backtest Pinia store（部分）
- ✅ 工具函数（format.ts, calculate.ts）
- ✅ MetricCard 组件

**待完成：**
- ❌ Layout 组件
- ❌ 路由配置
- ❌ 页面组件（Views）
- ❌ 图表组件
- ❌ 编辑器组件
- ❌ 组合式函数（composables）

### 1.3 开发分支
`feature/frontend-ui-framework`

---

## 2. 整体架构

### 2.1 目录结构
```
frontend/src/
├── components/
│   ├── layout/
│   │   ├── AppLayout.vue      # 主布局容器
│   │   ├── Header.vue         # 顶部导航栏
│   │   └── Sidebar.vue        # 左侧菜单
│   ├── common/
│   │   └── MetricCard.vue     # 已完成
│   ├── charts/
│   │   ├── EquityCurve.vue    # 权益曲线
│   │   ├── DrawdownChart.vue  # 回撤图
│   │   └── MonthlyReturns.vue # 月度收益热力图
│   └── editor/
│       └── CodeEditor.vue     # Monaco 编辑器封装
├── views/
│   ├── Dashboard.vue          # 仪表盘
│   ├── StrategyList.vue       # 策略列表
│   ├── StrategyEditor.vue     # 策略编辑
│   ├── BacktestConfig.vue     # 回测配置
│   ├── BacktestResult.vue     # 回测结果
│   └── Optimizer.vue          # 参数优化
├── router/
│   └── index.ts               # 路由配置
├── stores/
│   ├── backtest.ts            # 已完成
│   └── strategy.ts            # 待实现
├── composables/
│   ├── useBacktest.ts
│   ├── useStrategy.ts
│   └── useWebSocket.ts
├── api/                       # 已完成
├── types/                     # 已完成
└── utils/                     # 已完成
```

### 2.2 路由规划
| 路由 | 名称 | 页面 | 说明 |
|-----|------|------|------|
| `/` | - | 重定向 | 重定向到 /dashboard |
| `/dashboard` | Dashboard | Dashboard.vue | 仪表盘概览 |
| `/strategies` | StrategyList | StrategyList.vue | 策略列表 |
| `/strategies/new` | StrategyNew | StrategyEditor.vue | 新建策略 |
| `/strategies/:id/edit` | StrategyEdit | StrategyEditor.vue | 编辑策略 |
| `/backtest/config` | BacktestConfig | BacktestConfig.vue | 回测配置 |
| `/backtest/:id` | BacktestResult | BacktestResult.vue | 回测结果 |
| `/optimize` | Optimizer | Optimizer.vue | 参数优化 |

---

## 3. Layout 组件设计

### 3.1 布局结构
```
┌─────────────────────────────────────────────────────┐
│  Header (60px)                                       │
├──────────────┬──────────────────────────────────────┤
│              │                                       │
│  Sidebar     │  Main Content                        │
│  (200px)     │  (router-view)                       │
│              │                                       │
│              │                                       │
└──────────────┴──────────────────────────────────────┘
```

### 3.2 Header.vue
- 左侧：Logo + 应用名称 "AI Quant Platform"
- 中间：面包屑导航（可选）
- 右侧：用户信息预留位（可扩展）

### 3.3 Sidebar.vue
可折叠菜单，菜单项：
```
📊 仪表盘          → /dashboard
📝 策略管理        → /strategies
⚙️ 回测配置        → /backtest/config
📈 参数优化        → /optimize
```

**注意：** 新建策略按钮放在策略列表页面右上角，不在侧边栏做子菜单。

### 3.4 技术实现
- 使用 Element Plus 组件：`el-container`, `el-header`, `el-aside`, `el-menu`
- 响应式设计：移动端侧边栏可收起
- 菜单高亮跟随当前路由

---

## 4. 页面组件设计

### 4.1 Dashboard.vue - 仪表盘
```
┌─────────────────────────────────────────────────────────────────┐
│  工作台                                                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  │ 📊 策略总数  │  │ ⚡ 运行中    │  │ ✅ 近30天收益│  │ 📈 夏普比率  │
│  │     5      │  │     1      │  │   +15.2%   │  │    1.85    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
├─────────────────────────────────────────────────────────────────┤
│  快速操作                                                        │
│  [📝 新建策略]  [⚡ 快速回测]  [📊 查看报告]                       │
├─────────────────────────────────────────────────────────────────┤
│  最近回测                                                         │
│  ┌─────────────────────────────────────────────────────────────┐
│  │ 回测ID     策略名称     收益率    夏普    回撤     时间       │
│  │ bt_001    双均线MA     +23.5%   1.45   -12.3%   03-20 14:30 │
│  │ bt_002    RSI动量      +8.2%    0.92   -8.5%    03-19 10:15 │
│  └─────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

**功能要点：**
- 顶部统计卡片（4个 MetricCard）
- 快速操作按钮组
- 最近回测记录表格
- 点击记录跳转到详情页

### 4.2 StrategyList.vue - 策略列表
```
┌─────────────────────────────────────────────────────────────────┐
│  我的策略                                    [+ 新建策略]        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐
│  │ 策略名称      描述          创建时间      操作               │
│  ├─────────────────────────────────────────────────────────────┤
│  │ 双均线策略    MA金叉策略    03-01        [编辑][回测][删除]  │
│  │ RSI动量       RSI超卖反弹   03-15        [编辑][回测][删除]  │
│  └─────────────────────────────────────────────────────────────┘
│  显示 1-3 共 3 条                          [<] 1 [>]            │
└─────────────────────────────────────────────────────────────────┘
```

**功能要点：**
- 右上角"新建策略"按钮
- 表格展示策略列表
- 操作列：编辑、回测（跳转到配置页）、删除
- 分页控件

### 4.3 StrategyEditor.vue - 策略编辑器
```
┌─────────────────────────────────────────────────────────────────┐
│  新建策略 / 编辑策略                                 [保存] [回测]│
├─────────────────────────────────────────────────────────────────┤
│  策略名称: [________________]                                    │
│  描述:     [________________]                                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐
│  │  1 │ class MyStrategy(Strategy):                            │
│  │  2 │     """双均线策略"""                                    │
│  │  3 │     def on_bar(self, bar, engine):                     │
│  │  4 │         # 编写策略逻辑                                  │
│  │  5 │         pass                                           │
│  └─────────────────────────────────────────────────────────────┘
│  (Monaco Editor - Python语法高亮)                                │
└─────────────────────────────────────────────────────────────────┘
```

**功能要点：**
- 基础信息表单（名称、描述）
- Monaco Editor 代码编辑器
- Python 语法高亮
- 保存/回测按钮
- 编辑模式通过路由参数区分（/new vs /:id/edit）

### 4.4 BacktestConfig.vue - 回测配置
```
┌─────────────────────────────────────────────────────────────────┐
│  回测配置                                                        │
├─────────────────────────────────────────────────────────────────┤
│  选择策略:      [下拉选择]                                       │
│  交易标的:      [多选标的]                                       │
│  回测区间:      [开始日期] - [结束日期]                          │
│  初始资金:      [100000]                                        │
│  手续费率:      [0.0003]                                        │
│                                                                 │
│                                           [开始回测]             │
└─────────────────────────────────────────────────────────────────┘
```

**功能要点：**
- 策略下拉选择（从 store 获取）
- 标的多选（预设选项 + 搜索）
- 日期范围选择器
- 数值输入控件
- 提交后跳转到结果页

### 4.5 BacktestResult.vue - 回测结果
```
┌─────────────────────────────────────────────────────────────────┐
│  回测结果 - bt_001                           [导出] [重新回测]   │
│  策略: 双均线MA | 标的: 000001.SZ | 周期: 2023-01 ~ 2024-01     │
├─────────────────────────────────────────────────────────────────┤
│  [概览]  [交易记录]  [风险分析]  [每日收益]                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐    │
│  │ 总收益率    │ │ 年化收益    │ │ 最大回撤    │ │ 夏普比率    │    │
│  │ +23.45%   │ │ +18.20%   │ │ -12.30%   │ │   1.45    │    │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘    │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐    │
│  │ 胜率       │ │ 盈亏比      │ │ 交易次数    │ │ 基准收益    │    │
│  │  58.3%    │ │   1.85    │ │    42     │ │ +18.5%    │    │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘    │
├─────────────────────────────────────────────────────────────────┤
│  权益曲线                                                        │
│  [ECharts 图表区域]                                              │
├─────────────────────────────────────────────────────────────────┤
│  回撤分析                                                        │
│  [ECharts 图表区域]                                              │
└─────────────────────────────────────────────────────────────────┘
```

**Tab 页签说明：**
- **概览**：核心指标 + 权益曲线 + 回撤图（默认页）
- **交易记录**：详细交易列表，支持筛选/排序
- **风险分析**：月度收益热力图、持仓分析
- **每日收益**：每日收益分布图

**功能要点：**
- 8个 MetricCard 展示核心指标
- Tab 切换不同分析视图
- 权益曲线图（带基准线）
- 回撤图
- 交易记录表格

### 4.6 Optimizer.vue - 参数优化
```
┌─────────────────────────────────────────────────────────────────┐
│  参数优化                                                        │
├─────────────────────────────────────────────────────────────────┤
│  选择策略: [下拉选择]                                            │
│  交易标的: [多选标的]                                            │
│  回测区间: [开始日期] - [结束日期]                                │
├─────────────────────────────────────────────────────────────────┤
│  参数配置                                                        │
│  ┌─────────────────────────────────────────────────────────────┐
│  │ 参数名      范围(最小-最大)    步长                          │
│  │ fast_period  [5] - [30]       [1]                           │
│  │ slow_period  [20] - [60]      [5]                           │
│  │ [+ 添加参数]                                                │
│  └─────────────────────────────────────────────────────────────┘
├─────────────────────────────────────────────────────────────────┤
│  优化设置                                                        │
│  优化目标: [夏普比率 ▼]    最大迭代: [100]                       │
│                                                                 │
│                                              [开始优化]          │
├─────────────────────────────────────────────────────────────────┤
│  优化进度                                                         │
│  ████████████░░░░░░░░  60%  (60/100)                            │
│  当前最优: 夏普 1.85 | fast=12, slow=26                          │
├─────────────────────────────────────────────────────────────────┤
│  优化结果                                                         │
│  ┌─────────────────────────────────────────────────────────────┐
│  │ 排名   fast   slow   收益率    夏普    回撤                  │
│  │ 1      12     26     +25.3%   1.85    -10.2%                │
│  │ 2      10     25     +23.1%   1.72    -11.5%                │
│  │ 3      15     30     +21.8%   1.65    -9.8%                 │
│  └─────────────────────────────────────────────────────────────┘
│                                     [应用最优参数] [导出结果]    │
└─────────────────────────────────────────────────────────────────┘
```

**功能要点：**
- 参数动态配置（名称、范围、步长）
- 优化目标选择
- 进度条展示
- 结果表格排名
- 应用最优参数到策略

---

## 5. 图表组件设计

### 5.1 EquityCurve.vue - 权益曲线图
- **X轴**：日期
- **Y轴**：权益金额
- **主线**：策略权益曲线（蓝色渐变填充）
- **辅助线**：基准权益（灰色虚线）
- **交互**：鼠标悬停显示详细数值，tooltip 格式化

### 5.2 DrawdownChart.vue - 回撤图
- **X轴**：日期
- **Y轴**：回撤百分比（负值）
- **样式**：红色区域填充
- **标注**：最大回撤点标记

### 5.3 MonthlyReturns.vue - 月度收益热力图
- **行**：月份（1-12月）
- **列**：年份
- **颜色**：红色(正收益) → 白色(零) → 绿色(负收益)
- **数值**：月度收益率百分比

---

## 6. 技术实现要点

### 6.1 Element Plus 按需引入
```typescript
// main.ts
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)
app.use(ElementPlus, { locale: zhCn })

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
```

### 6.2 ECharts 配置
```typescript
// 使用 vue-echarts 封装
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { LineChart, BarChart, HeatmapChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([LineChart, BarChart, HeatmapChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])
```

### 6.3 Monaco Editor 集成
```typescript
// 使用 @monaco-editor/loader 或直接引入
import * as monaco from 'monaco-editor'
import 'monaco-editor/esm/vs/basic-languages/python/python.contribution'
```

---

## 7. 实现顺序

### Phase 1: Layout 组件（1天）
1. AppLayout.vue - 主布局容器
2. Header.vue - 顶部导航
3. Sidebar.vue - 左侧菜单

### Phase 2: 路由配置（0.5天）
1. router/index.ts - 路由定义
2. 路由守卫（页面标题）
3. 菜单高亮联动

### Phase 3: 页面占位（0.5天）
1. 创建所有页面组件（空白占位）
2. 验证路由跳转正常

### Phase 4: 页面实现（3天）
1. Dashboard.vue
2. StrategyList.vue + StrategyEditor.vue
3. BacktestConfig.vue + BacktestResult.vue
4. Optimizer.vue

### Phase 5: 图表组件（2天）
1. EquityCurve.vue
2. DrawdownChart.vue
3. MonthlyReturns.vue

### Phase 6: 补充完善（1天）
1. CodeEditor.vue
2. 补充 composables
3. 补充 strategy store
4. 整体测试

---

## 8. 验收标准

- [ ] Layout 正确显示，菜单可折叠
- [ ] 路由跳转正常，菜单高亮正确
- [ ] 所有页面可访问，无空白页
- [ ] Dashboard 展示统计数据
- [ ] 策略列表可新建/编辑/删除
- [ ] 回测配置可提交并跳转结果
- [ ] 回测结果展示图表和指标
- [ ] 参数优化流程完整
- [ ] 响应式布局在移动端可用

---

## 9. TypeScript 接口定义

### 9.1 Strategy Store

```typescript
// stores/strategy.ts
import { defineStore } from 'pinia'
import type { Strategy } from '@/types/api'

interface StrategyState {
  strategies: Strategy[]
  currentStrategy: Strategy | null
  isLoading: boolean
  error: string | null
}

export const useStrategyStore = defineStore('strategy', {
  state: (): StrategyState => ({
    strategies: [],
    currentStrategy: null,
    isLoading: false,
    error: null
  }),

  actions: {
    async fetchStrategies(): Promise<void>
    async fetchStrategy(id: string): Promise<Strategy>
    async createStrategy(data: { name: string; code: string; description?: string }): Promise<Strategy>
    async updateStrategy(id: string, data: Partial<Strategy>): Promise<Strategy>
    async deleteStrategy(id: string): Promise<void>
    setCurrentStrategy(strategy: Strategy | null): void
  }
})
```

### 9.2 组件 Props 定义

```typescript
// components/charts/EquityCurve.vue
interface EquityPoint {
  date: string
  equity: number
}

interface Props {
  data: EquityPoint[]
  baseline?: EquityPoint[]        // 可选基准线
  height?: string                 // 图表高度，默认 '400px'
}

// components/charts/DrawdownChart.vue
interface Props {
  equityCurve: number[]           // 权益数组
  dates: string[]                 // 对应日期
  height?: string
}

// components/charts/MonthlyReturns.vue
interface MonthlyReturn {
  year: number
  month: number
  return: number
}

interface Props {
  data: MonthlyReturn[]
  height?: string
}

// components/editor/CodeEditor.vue
interface Props {
  modelValue: string              // 代码内容
  language?: 'python' | 'javascript'
  readonly?: boolean
  height?: string
}

interface Emits {
  'update:modelValue': [value: string]
  'validate': [isValid: boolean, errors: string[]]
}

// views/StrategyEditor.vue
interface Props {
  strategyId?: string             // 编辑模式时传入
}

// views/BacktestResult.vue
interface Props {
  backtestId: string
}
```

---

## 10. 状态与错误处理

### 10.1 加载状态

所有页面组件需处理以下状态：

```typescript
// 页面级状态
const isLoading = ref(false)
const error = ref<string | null>(null)

// 空状态判断
const isEmpty = computed(() => data.value.length === 0)
```

### 10.2 空状态设计

| 组件 | 空状态提示 |
|-----|-----------|
| StrategyList | "暂无策略，点击右上角新建" |
| Dashboard 最近回测 | "暂无回测记录" |
| BacktestResult 交易记录 | "本次回测无交易记录" |

### 10.3 错误处理

```typescript
// composables/useAsync.ts - 通用异步处理
export function useAsync<T>(asyncFn: () => Promise<T>) {
  const data = ref<T | null>(null)
  const isLoading = ref(false)
  const error = ref<Error | null>(null)

  async function execute() {
    isLoading.value = true
    error.value = null
    try {
      data.value = await asyncFn()
    } catch (e) {
      error.value = e as Error
      ElMessage.error(error.value.message)
    } finally {
      isLoading.value = false
    }
  }

  return { data, isLoading, error, execute }
}
```

---

## 11. API 扩展

### 11.1 回测历史列表

```typescript
// api/backtest.ts 新增
export interface BacktestHistoryItem {
  backtest_id: string
  strategy_name: string
  status: 'running' | 'completed' | 'failed'
  total_return: number
  sharpe_ratio: number
  max_drawdown: number
  created_at: string
}

export const backtestApi = {
  // 已有
  run: (request: BacktestRequest) => Promise<BacktestRunResponse>,
  getResult: (id: string) => Promise<BacktestResult>,
  getStatus: (id: string) => Promise<BacktestStatusResponse>,

  // 新增
  list: (params?: { limit?: number; offset?: number }) => Promise<{
    items: BacktestHistoryItem[]
    total: number
  }>
}
```

### 11.2 仪表盘统计

```typescript
// api/dashboard.ts 新增
export interface DashboardStats {
  strategy_count: number
  running_count: number
  return_30d: number
  avg_sharpe: number
}

export const dashboardApi = {
  getStats: () => Promise<DashboardStats>
}
```

### 11.3 月度收益数据结构

```typescript
// types/api.ts 扩展
export interface MonthlyReturn {
  year: number
  month: number      // 1-12
  return: number     // 月度收益率
}

// BacktestResult 新增字段
export interface BacktestResult {
  // ... 已有字段
  monthly_returns: MonthlyReturn[]  // 新增
}
```

---

## 12. 组件交互流程

### 12.1 策略编辑流程

```
StrategyList
    │
    ├─ 点击 [新建] ──────────────► /strategies/new
    │                               │
    │                               ▼
    │                          StrategyEditor (新建模式)
    │                               │
    │                               ├─ 保存 → 返回列表
    │                               └─ 回测 → 跳转 BacktestConfig (预选策略)
    │
    └─ 点击 [编辑] ──────────────► /strategies/:id/edit
                                    │
                                    ▼
                               StrategyEditor (编辑模式)
                                    │
                                    ├─ 通过 route.params.id 获取策略
                                    └─ 保存后更新列表
```

### 12.2 回测流程

```
BacktestConfig
    │
    ├─ 选择策略 (从 strategyStore.strategies)
    ├─ 配置参数
    └─ 提交 ──► backtestStore.runBacktest()
                    │
                    ▼
              /backtest/:id  (BacktestResult)
                    │
                    ├─ 轮询状态 (status === 'running')
                    │     └─ 每 2 秒调用 getStatus()
                    │
                    └─ 加载结果 (status === 'completed')
                          └─ getResult() 获取完整数据
```

### 12.3 参数优化流程

```
Optimizer
    │
    ├─ 选择策略
    ├─ 配置参数范围 (动态添加)
    ├─ 提交 ──► optimizeApi.start()
    │
    └─ 监听进度
          │
          ├─ WebSocket 连接 (ws://host/ws/optimize/:id)
          │     └─ 接收 { type: 'progress', trial: 60, total: 100, best: {...} }
          │
          └─ 完成后展示结果表格
                └─ [应用最优参数] → 更新策略代码
```

---

## 13. WebSocket 实时通信

### 13.1 连接管理

```typescript
// composables/useWebSocket.ts
export function useWebSocket() {
  const ws = ref<WebSocket | null>(null)
  const isConnected = ref(false)
  const lastMessage = ref<any>(null)

  function connect(url: string): Promise<void> {
    return new Promise((resolve, reject) => {
      ws.value = new WebSocket(url)

      ws.value.onopen = () => {
        isConnected.value = true
        resolve()
      }

      ws.value.onerror = (error) => {
        reject(error)
      }

      ws.value.onmessage = (event) => {
        lastMessage.value = JSON.parse(event.data)
      }
    })
  }

  function disconnect(): void {
    ws.value?.close()
    ws.value = null
    isConnected.value = false
  }

  function onMessage(handler: (data: any) => void): void {
    // 注册消息处理器
  }

  onUnmounted(() => disconnect())

  return { connect, disconnect, isConnected, lastMessage, onMessage }
}
```

### 13.2 消息类型

```typescript
// 优化进度消息
interface OptimizationProgressMessage {
  type: 'progress'
  trial: number
  total: number
  best_value: number
  best_params: Record<string, number>
}

// 回测进度消息
interface BacktestProgressMessage {
  type: 'progress'
  current: number
  total: number
  message: string
}
```

### 13.3 降级策略

WebSocket 不可用时，使用 HTTP 轮询：

```typescript
// composables/usePolling.ts
export function usePolling<T>(
  fetchFn: () => Promise<T>,
  interval: number = 2000,
  condition: (data: T) => boolean = () => true
) {
  const data = ref<T | null>(null)
  const isPolling = ref(false)

  async function start() {
    isPolling.value = true
    while (isPolling.value) {
      data.value = await fetchFn()
      if (!condition(data.value)) break
      await new Promise(r => setTimeout(r, interval))
    }
  }

  function stop() {
    isPolling.value = false
  }

  return { data, isPolling, start, stop }
}
```

---

## 14. Monaco Editor 配置

### 14.1 Vite 集成

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  worker: {
    format: 'es'
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          monaco: ['monaco-editor']
        }
      }
    }
  }
})
```

### 14.2 Worker 配置

```typescript
// components/editor/CodeEditor.vue
import * as monaco from 'monaco-editor'
import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker'
import python from 'monaco-editor/esm/vs/basic-languages/python/python?worker'

// 配置 Worker
self.MonacoEnvironment = {
  getWorker() {
    return new editorWorker()
  }
}

// Python 语法支持
monaco.languages.register({ id: 'python' })
```

### 14.3 默认策略模板

```python
# 默认模板
class MyStrategy(Strategy):
    """策略描述"""

    # 参数定义
    fast_period = 10
    slow_period = 30

    def on_bar(self, bar: Bar, engine: Engine):
        """每根K线触发"""
        # 获取指标
        fast_ma = engine.indicator('MA', period=self.fast_period)
        slow_ma = engine.indicator('MA', period=self.slow_period)

        # 交易逻辑
        if fast_ma > slow_ma:
            engine.submit_order(Order(side='buy', symbol=bar.symbol, quantity=100))
        elif fast_ma < slow_ma:
            engine.submit_order(Order(side='sell', symbol=bar.symbol, quantity=100))
```

---

## 15. 实现顺序（更新）

### Phase 0: 基础设施（0.5天）
1. 扩展 types/api.ts（新增类型定义）
2. 创建 api/dashboard.ts
3. 扩展 api/backtest.ts（list 方法）

### Phase 1: Store 完善（0.5天）
1. strategy.ts store 完整实现
2. backtest.ts store 扩展（历史记录）

### Phase 2: Layout 组件（1天）
1. AppLayout.vue
2. Header.vue
3. Sidebar.vue

### Phase 3: 路由配置（0.5天）
1. router/index.ts
2. 路由守卫

### Phase 4: 页面占位（0.5天）
1. 所有页面空白占位

### Phase 5: 页面实现（3天）
1. Dashboard.vue
2. StrategyList.vue + StrategyEditor.vue
3. BacktestConfig.vue + BacktestResult.vue
4. Optimizer.vue

### Phase 6: 图表组件（2天）
1. EquityCurve.vue
2. DrawdownChart.vue
3. MonthlyReturns.vue

### Phase 7: 补充完善（1天）
1. CodeEditor.vue
2. composables（useWebSocket, usePolling）
3. 整体测试