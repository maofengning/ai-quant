# Frontend Implementation Plan - Quant Platform

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build Vue3 frontend with TDD for quantitative backtesting platform, using MSW to mock backend API during development.

**Architecture:** Component-based architecture with Pinia state management, ECharts visualization, Monaco editor for strategy code, and MSW for API mocking during parallel development.

**Tech Stack:** Vue3, Vite, Vitest, Pinia, Element Plus, ECharts, Monaco Editor, MSW, TypeScript

---

## File Structure

```
frontend/
├── package.json                # Dependencies
├── vite.config.ts             # Vite configuration
├── vitest.config.ts           # Vitest configuration
├── tsconfig.json              # TypeScript config
├── index.html
├── src/
│   ├── main.ts                # Application entry
│   ├── App.vue                # Root component
│   ├── router/
│   │   └── index.ts           # Vue Router config
│   ├── stores/
│   │   ├── index.ts
│   │   ├── backtest.ts        # Backtest state
│   │   └── strategy.ts        # Strategy state
│   ├── api/
│   │   ├── client.ts          # Axios client
│   │   ├── backtest.ts        # Backtest API
│   │   └── strategy.ts        # Strategy API
│   ├── types/
│   │   └── api.ts             # API types
│   ├── composables/
│   │   ├── useBacktest.ts     # Backtest logic
│   │   └── useChart.ts        # Chart configuration
│   ├── components/
│   │   ├── common/
│   │   │   ├── MetricCard.vue # Metric display card
│   │   │   └── DataTable.vue  # Data table
│   │   ├── charts/
│   │   │   ├── EquityCurve.vue     # Equity curve chart
│   │   │   └── DrawdownChart.vue   # Drawdown chart
│   │   └── editor/
│   │       └── CodeEditor.vue      # Monaco editor wrapper
│   ├── views/
│   │   ├── Dashboard.vue           # Dashboard page
│   │   ├── StrategyEditor.vue      # Strategy editor
│   │   ├── BacktestConfig.vue      # Backtest config
│   │   └── BacktestResult.vue      # Result display
│   ├── utils/
│   │   ├── format.ts          # Format utilities
│   │   └── calculate.ts       # Calculation utilities
│   ├── mocks/
│   │   ├── browser.ts         # MSW browser setup
│   │   ├── handlers.ts        # API mock handlers
│   │   └── data/
│   │       ├── strategies.ts  # Mock strategy data
│   │       └── backtest.ts    # Mock backtest data
│   └── assets/
│       └── styles/
│           └── main.css
└── tests/
    ├── setup.ts               # Test setup
    ├── unit/
    │   ├── components/
    │   ├── composables/
    │   └── utils/
    └── integration/
        └── views/
```

---

## Task 1: Project Initialization

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/vitest.config.ts`
- Create: `frontend/tsconfig.json`
- Create: `frontend/index.html`
- Create: `frontend/src/main.ts`
- Create: `frontend/tests/setup.ts`

- [ ] **Step 1: Create project with Vite**

```bash
cd /Users/maofengning/work/project/aicoding/ai-quant
npm create vite@latest frontend -- --template vue-ts
cd frontend
```

- [ ] **Step 2: Install dependencies**

```bash
npm install vue@^3.4.0 vue-router@^4.3.0 pinia@^2.1.0
npm install element-plus@^2.6.0 @element-plus/icons-vue@^2.3.0
npm install echarts@^5.5.0 vue-echarts@^6.7.0
npm install monaco-editor@^0.47.0
npm install axios@^1.6.0 dayjs@^1.11.0

npm install -D vitest@^1.4.0 @vitest/ui@^1.4.0
npm install -D @vue/test-utils@^2.4.0 @testing-library/vue@^8.0.0
npm install -D jsdom@^24.0.0 happy-dom@^14.0.0
npm install -D msw@^2.2.0
npm install -D @types/node
```

- [ ] **Step 3: Configure Vitest**

Create: `frontend/vitest.config.ts`

```typescript
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mocks/**'
      ],
      thresholds: {
        lines: 75,
        functions: 75,
        branches: 75,
        statements: 75
      }
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
```

- [ ] **Step 4: Create test setup**

Create: `frontend/tests/setup.ts`

```typescript
import { vi } from 'vitest'
import { config } from '@vue/test-utils'

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn()
  }))
})

// Configure Vue Test Utils
config.global.stubs = {
  teleport: true
}
```

- [ ] **Step 5: Update package.json scripts**

Modify: `frontend/package.json` (add to scripts section)

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "lint": "eslint . --ext .vue,.ts,.tsx --fix"
  }
}
```

- [ ] **Step 6: Create basic main.ts**

Create: `frontend/src/main.ts`

```typescript
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
app.mount('#app')
```

Create: `frontend/src/App.vue`

```vue
<template>
  <div id="app">
    <h1>AI Quant Platform</h1>
  </div>
</template>
```

- [ ] **Step 7: Verify setup works**

```bash
cd frontend
npm run test
```

Expected: Vitest runs (no tests yet)

- [ ] **Step 8: Verify dev server**

```bash
cd frontend
npm run dev &
sleep 2
curl http://localhost:5173/
pkill -f vite
```

Expected: HTML response

- [ ] **Step 9: Commit**

```bash
git add frontend/
git commit -m "feat: initialize frontend project with Vite and Vitest

- Setup Vue3 + TypeScript + Vite
- Configure Vitest with jsdom environment
- Install Element Plus, ECharts, Monaco Editor
- Add test setup and scripts

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 2: MSW Mock Setup

**Files:**
- Create: `frontend/src/mocks/browser.ts`
- Create: `frontend/src/mocks/handlers.ts`
- Create: `frontend/src/mocks/data/strategies.ts`
- Create: `frontend/src/mocks/data/backtest.ts`

- [ ] **Step 1: Create mock data - strategies**

Create: `frontend/src/mocks/data/strategies.ts`

```typescript
export const mockStrategies = [
  {
    strategy_id: 'strat_001',
    name: 'MA Crossover',
    code: `class MACrossover(Strategy):
    def on_bar(self, bar, engine):
        # Simple MA crossover strategy
        pass`,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z'
  },
  {
    strategy_id: 'strat_002',
    name: 'RSI Strategy',
    code: `class RSIStrategy(Strategy):
    def on_bar(self, bar, engine):
        # RSI-based strategy
        pass`,
    created_at: '2024-01-02T00:00:00Z',
    updated_at: '2024-01-02T00:00:00Z'
  }
]
```

Create: `frontend/src/mocks/data/backtest.ts`

```typescript
export const mockBacktestResult = {
  backtest_id: 'bt_test_001',
  status: 'completed',
  summary: {
    total_return: 0.23,
    annual_return: 0.18,
    max_drawdown: -0.12,
    sharpe_ratio: 1.45,
    win_rate: 0.58
  },
  equity_curve: [
    { date: '2023-01-01', equity: 100000 },
    { date: '2023-02-01', equity: 105000 },
    { date: '2023-03-01', equity: 110000 },
    { date: '2023-04-01', equity: 115000 },
    { date: '2023-05-01', equity: 123000 }
  ],
  trades: [
    {
      datetime: '2023-01-15T09:30:00',
      symbol: '000001.SZ',
      side: 'buy',
      quantity: 100,
      price: 10.0,
      pnl: 0
    },
    {
      datetime: '2023-02-20T15:00:00',
      symbol: '000001.SZ',
      side: 'sell',
      quantity: 100,
      price: 12.0,
      pnl: 200
    }
  ],
  daily_returns: []
}
```

- [ ] **Step 2: Create MSW handlers**

Create: `frontend/src/mocks/handlers.ts`

```typescript
import { http, HttpResponse } from 'msw'
import { mockStrategies } from './data/strategies'
import { mockBacktestResult } from './data/backtest'

export const handlers = [
  // Get symbols
  http.get('/api/v1/data/symbols', ({ request }) => {
    const url = new URL(request.url)
    const market = url.searchParams.get('market')

    if (market === 'cn_stock') {
      return HttpResponse.json({
        market,
        symbols: ['000001.SZ', '000002.SZ', '600000.SH']
      })
    }
    return HttpResponse.json({ market, symbols: [] })
  }),

  // Get strategies
  http.get('/api/v1/strategies', () => {
    return HttpResponse.json({ strategies: mockStrategies })
  }),

  // Create strategy
  http.post('/api/v1/strategies', async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json({
      strategy_id: `strat_${Date.now()}`,
      ...body,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }, { status: 201 })
  }),

  // Run backtest
  http.post('/api/v1/backtest/run', async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json({
      backtest_id: `bt_${Date.now()}`,
      status: 'running'
    })
  }),

  // Get backtest result
  http.get('/api/v1/backtest/:id/result', ({ params }) => {
    return HttpResponse.json(mockBacktestResult)
  }),

  // Get backtest status
  http.get('/api/v1/backtest/:id/status', ({ params }) => {
    return HttpResponse.json({
      backtest_id: params.id,
      status: 'completed',
      progress: 100
    })
  })
]
```

- [ ] **Step 3: Setup MSW browser**

Create: `frontend/src/mocks/browser.ts`

```typescript
import { setupWorker } from 'msw/browser'
import { handlers } from './handlers'

export const worker = setupWorker(...handlers)
```

- [ ] **Step 4: Initialize MSW in development**

Modify: `frontend/src/main.ts`

```typescript
import { createApp } from 'vue'
import App from './App.vue'

async function enableMocking() {
  if (import.meta.env.MODE === 'development') {
    const { worker } = await import('./mocks/browser')
    return worker.start({
      onUnhandledRequest: 'bypass'
    })
  }
}

enableMocking().then(() => {
  const app = createApp(App)
  app.mount('#app')
})
```

- [ ] **Step 5: Add MSW public files**

```bash
cd frontend
npx msw init public/ --save
```

Expected: Creates `public/mockServiceWorker.js`

- [ ] **Step 6: Test MSW in browser**

```bash
cd frontend
npm run dev
```

Open browser to `http://localhost:5173` and check console for MSW message

- [ ] **Step 7: Commit**

```bash
git add frontend/src/mocks/ frontend/public/ frontend/src/main.ts
git commit -m "feat: setup MSW for API mocking

- Create mock handlers for data, strategies, backtest APIs
- Add mock data for strategies and backtest results
- Initialize MSW worker in development mode
- Add mockServiceWorker.js to public/

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 3: API Client and Types

**Files:**
- Create: `frontend/src/types/api.ts`
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/api/backtest.ts`
- Create: `frontend/tests/unit/api/backtest.test.ts`

- [ ] **Step 1: Write failing test for backtest API**

Create: `frontend/tests/unit/api/backtest.test.ts`

```typescript
import { describe, it, expect, beforeAll, afterEach, afterAll } from 'vitest'
import { setupServer } from 'msw/node'
import { handlers } from '@/mocks/handlers'
import { backtestApi } from '@/api/backtest'

const server = setupServer(...handlers)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('Backtest API', () => {
  it('should start backtest and return backtest_id', async () => {
    const request = {
      strategy_id: 'test_strat',
      symbols: ['000001.SZ'],
      start_date: '2023-01-01',
      end_date: '2024-01-01',
      initial_capital: 100000,
      commission: 0.0003
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

- [ ] **Step 2: Run test to verify it fails**

```bash
cd frontend
npm run test backtest.test.ts
```

Expected: FAIL with module not found

- [ ] **Step 3: Create API types**

Create: `frontend/src/types/api.ts`

```typescript
export interface BacktestRequest {
  strategy_id: string
  symbols: string[]
  start_date: string
  end_date: string
  initial_capital: number
  commission?: number
  slippage?: number
}

export interface BacktestRunResponse {
  backtest_id: string
  status: 'running' | 'completed' | 'failed'
}

export interface EquityPoint {
  date: string
  equity: number
}

export interface Trade {
  datetime: string
  symbol: string
  side: 'buy' | 'sell'
  quantity: number
  price: number
  pnl: number
}

export interface BacktestSummary {
  total_return: number
  annual_return: number
  max_drawdown: number
  sharpe_ratio: number
  win_rate: number
}

export interface BacktestResult {
  backtest_id: string
  status: 'running' | 'completed' | 'failed'
  summary: BacktestSummary
  equity_curve: EquityPoint[]
  trades: Trade[]
  daily_returns: number[]
}

export interface Strategy {
  strategy_id: string
  name: string
  code: string
  created_at: string
  updated_at: string
}

export interface StrategyListResponse {
  strategies: Strategy[]
}
```

- [ ] **Step 4: Create API client**

Create: `frontend/src/api/client.ts`

```typescript
import axios from 'axios'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
apiClient.interceptors.request.use(
  config => {
    // Add auth token if available
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Response interceptor
apiClient.interceptors.response.use(
  response => response,
  error => {
    // Handle errors globally
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)
```

- [ ] **Step 5: Implement backtest API**

Create: `frontend/src/api/backtest.ts`

```typescript
import { apiClient } from './client'
import type {
  BacktestRequest,
  BacktestRunResponse,
  BacktestResult
} from '@/types/api'

export const backtestApi = {
  /**
   * Start a new backtest.
   */
  async run(request: BacktestRequest): Promise<BacktestRunResponse> {
    const { data } = await apiClient.post('/backtest/run', request)
    return data
  },

  /**
   * Get backtest result.
   */
  async getResult(backtestId: string): Promise<BacktestResult> {
    const { data } = await apiClient.get(`/backtest/${backtestId}/result`)
    return data
  },

  /**
   * Get backtest status.
   */
  async getStatus(backtestId: string) {
    const { data } = await apiClient.get(`/backtest/${backtestId}/status`)
    return data
  }
}
```

- [ ] **Step 6: Run tests**

```bash
cd frontend
npm run test backtest.test.ts
```

Expected: All 2 tests PASS

- [ ] **Step 7: Commit**

```bash
git add frontend/src/types/ frontend/src/api/ frontend/tests/unit/api/
git commit -m "feat: add API client and backtest API

- Create TypeScript types for API requests/responses
- Implement axios client with interceptors
- Add backtestApi with run/getResult/getStatus methods
- 2 tests for backtest API with MSW

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 4: Utility Functions

**Files:**
- Create: `frontend/src/utils/format.ts`
- Create: `frontend/src/utils/calculate.ts`
- Create: `frontend/tests/unit/utils/format.test.ts`
- Create: `frontend/tests/unit/utils/calculate.test.ts`

- [ ] **Step 1: Write failing tests for format utils**

Create: `frontend/tests/unit/utils/format.test.ts`

```typescript
import { describe, it, expect } from 'vitest'
import { formatPercent, formatCurrency, formatDate } from '@/utils/format'

describe('Format Utils', () => {
  describe('formatPercent', () => {
    it('should format positive percentage', () => {
      expect(formatPercent(0.1234)).toBe('12.34%')
    })

    it('should format negative percentage', () => {
      expect(formatPercent(-0.056)).toBe('-5.60%')
    })

    it('should format large percentage', () => {
      expect(formatPercent(1.5)).toBe('150.00%')
    })

    it('should format with custom decimals', () => {
      expect(formatPercent(0.12345, 3)).toBe('12.345%')
    })
  })

  describe('formatCurrency', () => {
    it('should format currency with Chinese Yuan symbol', () => {
      expect(formatCurrency(100000)).toBe('¥100,000.00')
    })

    it('should format large numbers with commas', () => {
      expect(formatCurrency(1234567.89)).toBe('¥1,234,567.89')
    })

    it('should format zero', () => {
      expect(formatCurrency(0)).toBe('¥0.00')
    })
  })

  describe('formatDate', () => {
    it('should format date string', () => {
      expect(formatDate('2024-01-01')).toBe('2024-01-01')
    })

    it('should format datetime string', () => {
      const result = formatDate('2024-01-01T09:30:00')
      expect(result).toContain('2024')
      expect(result).toContain('09:30')
    })
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd frontend
npm run test format.test.ts
```

Expected: FAIL with module not found

- [ ] **Step 3: Implement format utils**

Create: `frontend/src/utils/format.ts`

```typescript
/**
 * Format a decimal value as percentage.
 */
export function formatPercent(value: number, decimals: number = 2): string {
  return (value * 100).toFixed(decimals) + '%'
}

/**
 * Format a number as currency (Chinese Yuan).
 */
export function formatCurrency(value: number): string {
  return '¥' + value.toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

/**
 * Format date string for display.
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString)

  // If time is included, format with time
  if (dateString.includes('T') || dateString.includes(' ')) {
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    }).replace(/\//g, '-')
  }

  // Otherwise just date
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).replace(/\//g, '-')
}
```

- [ ] **Step 4: Run format tests**

```bash
cd frontend
npm run test format.test.ts
```

Expected: All tests PASS

- [ ] **Step 5: Write failing tests for calculate utils**

Create: `frontend/tests/unit/utils/calculate.test.ts`

```typescript
import { describe, it, expect } from 'vitest'
import { calculateMaxDrawdown, calculateWinRate } from '@/utils/calculate'

describe('Calculate Utils', () => {
  describe('calculateMaxDrawdown', () => {
    it('should calculate max drawdown', () => {
      const equity = [100000, 110000, 105000, 95000, 100000]
      const maxDD = calculateMaxDrawdown(equity)

      // Max drawdown from 110000 to 95000 = -13.636%
      expect(maxDD).toBeCloseTo(-0.1364, 3)
    })

    it('should return 0 for monotonically increasing equity', () => {
      const equity = [100000, 110000, 120000, 130000]
      const maxDD = calculateMaxDrawdown(equity)

      expect(maxDD).toBe(0)
    })

    it('should handle empty array', () => {
      const maxDD = calculateMaxDrawdown([])
      expect(maxDD).toBe(0)
    })
  })

  describe('calculateWinRate', () => {
    it('should calculate win rate', () => {
      const trades = [
        { pnl: 100 },
        { pnl: -50 },
        { pnl: 200 },
        { pnl: -30 }
      ]
      const winRate = calculateWinRate(trades)

      expect(winRate).toBe(0.5) // 2 out of 4 = 50%
    })

    it('should return 1 for all wins', () => {
      const trades = [{ pnl: 100 }, { pnl: 200 }]
      expect(calculateWinRate(trades)).toBe(1)
    })

    it('should return 0 for all losses', () => {
      const trades = [{ pnl: -100 }, { pnl: -200 }]
      expect(calculateWinRate(trades)).toBe(0)
    })

    it('should handle empty trades', () => {
      expect(calculateWinRate([])).toBe(0)
    })
  })
})
```

- [ ] **Step 6: Run test to verify it fails**

```bash
cd frontend
npm run test calculate.test.ts
```

Expected: FAIL with module not found

- [ ] **Step 7: Implement calculate utils**

Create: `frontend/src/utils/calculate.ts`

```typescript
/**
 * Calculate maximum drawdown from equity curve.
 */
export function calculateMaxDrawdown(equityCurve: number[]): number {
  if (equityCurve.length === 0) return 0

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

/**
 * Calculate win rate from trades.
 */
export function calculateWinRate(trades: Array<{ pnl: number }>): number {
  if (trades.length === 0) return 0

  const winningTrades = trades.filter(t => t.pnl > 0).length
  return winningTrades / trades.length
}

/**
 * Calculate Sharpe ratio from returns.
 */
export function calculateSharpeRatio(
  returns: number[],
  riskFreeRate: number = 0.03
): number {
  if (returns.length === 0) return 0

  const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length
  const variance = returns.reduce(
    (sum, r) => sum + Math.pow(r - avgReturn, 2),
    0
  ) / returns.length
  const stdDev = Math.sqrt(variance)

  if (stdDev === 0) return 0

  // Annualize (assuming daily returns, 252 trading days)
  return (avgReturn * 252 - riskFreeRate) / (stdDev * Math.sqrt(252))
}
```

- [ ] **Step 8: Run calculate tests**

```bash
cd frontend
npm run test calculate.test.ts
```

Expected: All tests PASS

- [ ] **Step 9: Commit**

```bash
git add frontend/src/utils/ frontend/tests/unit/utils/
git commit -m "feat: add utility functions for formatting and calculations

- Add formatPercent, formatCurrency, formatDate functions
- Add calculateMaxDrawdown, calculateWinRate functions
- 13 tests covering all utility functions

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 5: Pinia Stores

**Files:**
- Create: `frontend/src/stores/index.ts`
- Create: `frontend/src/stores/backtest.ts`
- Create: `frontend/tests/unit/stores/backtest.test.ts`
- Modify: `frontend/src/main.ts`

- [ ] **Step 1: Write failing test for backtest store**

Create: `frontend/tests/unit/stores/backtest.test.ts`

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
      initial_capital: 100000,
      commission: 0.0003
    }

    await store.runBacktest(config)

    expect(store.currentBacktest).not.toBeNull()
    expect(store.currentBacktest?.backtest_id).toBeDefined()
  })

  it('should compute total return percentage', () => {
    const store = useBacktestStore()
    store.currentBacktest = {
      backtest_id: 'test',
      status: 'completed',
      summary: {
        total_return: 0.23,
        annual_return: 0.18,
        max_drawdown: -0.12,
        sharpe_ratio: 1.45,
        win_rate: 0.58
      },
      equity_curve: [],
      trades: [],
      daily_returns: []
    }

    expect(store.totalReturnPercent).toBe('23.00%')
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd frontend
npm run test backtest.test.ts
```

Expected: FAIL with module not found

- [ ] **Step 3: Create stores index**

Create: `frontend/src/stores/index.ts`

```typescript
import { createPinia } from 'pinia'

export const pinia = createPinia()
```

- [ ] **Step 4: Implement backtest store**

Create: `frontend/src/stores/backtest.ts`

```typescript
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

  const maxDrawdownPercent = computed(() => {
    if (!currentBacktest.value?.summary.max_drawdown) return '0.00%'
    return (currentBacktest.value.summary.max_drawdown * 100).toFixed(2) + '%'
  })

  // Actions
  async function runBacktest(config: BacktestRequest) {
    isRunning.value = true
    try {
      const response = await backtestApi.run(config)

      // Create placeholder result
      currentBacktest.value = {
        backtest_id: response.backtest_id,
        status: response.status,
        summary: {
          total_return: 0,
          annual_return: 0,
          max_drawdown: 0,
          sharpe_ratio: 0,
          win_rate: 0
        },
        equity_curve: [],
        trades: [],
        daily_returns: []
      }

      return response
    } catch (error) {
      console.error('Failed to run backtest:', error)
      throw error
    } finally {
      isRunning.value = false
    }
  }

  async function fetchResult(backtestId: string) {
    try {
      const result = await backtestApi.getResult(backtestId)
      currentBacktest.value = result

      // Update in list
      const index = backtests.value.findIndex(b => b.backtest_id === backtestId)
      if (index !== -1) {
        backtests.value[index] = result
      } else {
        backtests.value.push(result)
      }

      return result
    } catch (error) {
      console.error('Failed to fetch backtest result:', error)
      throw error
    }
  }

  return {
    backtests,
    currentBacktest,
    isRunning,
    totalReturnPercent,
    maxDrawdownPercent,
    runBacktest,
    fetchResult
  }
})
```

- [ ] **Step 5: Register Pinia in main.ts**

Modify: `frontend/src/main.ts`

```typescript
import { createApp } from 'vue'
import { pinia } from './stores'
import App from './App.vue'

async function enableMocking() {
  if (import.meta.env.MODE === 'development') {
    const { worker } = await import('./mocks/browser')
    return worker.start({
      onUnhandledRequest: 'bypass'
    })
  }
}

enableMocking().then(() => {
  const app = createApp(App)
  app.use(pinia)
  app.mount('#app')
})
```

- [ ] **Step 6: Run tests**

```bash
cd frontend
npm run test stores/backtest.test.ts
```

Expected: All 3 tests PASS

- [ ] **Step 7: Commit**

```bash
git add frontend/src/stores/ frontend/tests/unit/stores/ frontend/src/main.ts
git commit -m "feat: add Pinia store for backtest state

- Create backtest store with runBacktest and fetchResult actions
- Add computed properties for formatted return/drawdown
- Register Pinia in main.ts
- 3 tests for backtest store

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 6: Metric Card Component

**Files:**
- Create: `frontend/src/components/common/MetricCard.vue`
- Create: `frontend/tests/unit/components/MetricCard.test.ts`

- [ ] **Step 1: Write failing test**

Create: `frontend/tests/unit/components/MetricCard.test.ts`

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MetricCard from '@/components/common/MetricCard.vue'

describe('MetricCard', () => {
  it('should render label and value', () => {
    const wrapper = mount(MetricCard, {
      props: {
        label: '总收益率',
        value: '23.45%'
      }
    })

    expect(wrapper.text()).toContain('总收益率')
    expect(wrapper.text()).toContain('23.45%')
  })

  it('should apply positive class for up trend', () => {
    const wrapper = mount(MetricCard, {
      props: {
        label: '收益',
        value: '12.3%',
        trend: 'up'
      }
    })

    expect(wrapper.find('.metric-value').classes()).toContain('positive')
  })

  it('should apply negative class for down trend', () => {
    const wrapper = mount(MetricCard, {
      props: {
        label: '回撤',
        value: '-8.5%',
        trend: 'down'
      }
    })

    expect(wrapper.find('.metric-value').classes()).toContain('negative')
  })

  it('should render description when provided', () => {
    const wrapper = mount(MetricCard, {
      props: {
        label: 'Sharpe',
        value: '1.45',
        description: '风险调整后收益'
      }
    })

    expect(wrapper.text()).toContain('风险调整后收益')
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd frontend
npm run test MetricCard.test.ts
```

Expected: FAIL with component not found

- [ ] **Step 3: Create directory**

```bash
mkdir -p frontend/src/components/common
```

- [ ] **Step 4: Implement MetricCard component**

Create: `frontend/src/components/common/MetricCard.vue`

```vue
<template>
  <div class="metric-card">
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
  </div>
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
  padding: 16px;
  text-align: center;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.metric-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
}

.metric-value.positive {
  color: #67c23a;
}

.metric-value.negative {
  color: #f56c6c;
}

.metric-value.neutral {
  color: #303133;
}

.metric-description {
  font-size: 12px;
  color: #999;
}
</style>
```

- [ ] **Step 5: Run tests**

```bash
cd frontend
npm run test MetricCard.test.ts
```

Expected: All 4 tests PASS

- [ ] **Step 6: Commit**

```bash
git add frontend/src/components/common/ frontend/tests/unit/components/
git commit -m "feat: add MetricCard component

- Create reusable metric display card
- Support trend styling (positive/negative/neutral)
- Add optional description field
- 4 tests covering rendering and styling

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Next Steps

Continue with remaining tasks following TDD:

- Task 7: Router setup
- Task 8: Dashboard view
- Task 9: Strategy editor view
- Task 10: Backtest config view
- Task 11: Backtest result view with charts
- Task 12: Equity curve chart component
- Task 13: Drawdown chart component
- Task 14: End-to-end workflow test

---

## Execution Options

Plan complete and saved to `docs/superpowers/plans/2026-03-23-frontend-implementation.md`.

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration. Use @superpowers:subagent-driven-development

**2. Inline Execution** - Execute tasks in this session using @superpowers:executing-plans, batch execution with checkpoints

**Which approach?**
