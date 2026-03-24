# Layout and Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the core layout structure (header, sidebar, main content area) and dashboard homepage with navigation routing per spec `/Users/maofengning/work/project/aicoding/ai-quant/docs/superpowers/specs/2026-03-23-frontend-ui-design.md`.

**Architecture:** Vue 3 Composition API with Vue Router and Element Plus UI framework. Layout uses Element Plus container components (`el-container`, `el-header`, `el-aside`, `el-menu`). Dashboard displays 4 stat cards + quick actions + recent backtest table.

**Tech Stack:** Vue 3, TypeScript, Vue Router, Pinia, Element Plus, Vitest, Testing Library

---

## File Structure

**New Files:**
- `frontend/src/components/layout/Header.vue` - Top navigation bar with branding (Element Plus)
- `frontend/src/components/layout/Sidebar.vue` - Left sidebar navigation menu (Element Plus el-menu)
- `frontend/src/components/layout/AppLayout.vue` - Main layout wrapper using el-container
- `frontend/src/views/Dashboard.vue` - Dashboard homepage with 4 stat cards + quick actions + recent backtest table
- `frontend/src/router/index.ts` - Vue Router configuration (7 routes per spec)
- `frontend/tests/unit/components/layout/Header.test.ts` - Header component tests
- `frontend/tests/unit/components/layout/Sidebar.test.ts` - Sidebar component tests
- `frontend/tests/unit/components/layout/AppLayout.test.ts` - Layout component tests
- `frontend/tests/unit/views/Dashboard.test.ts` - Dashboard view tests

**Modified Files:**
- `frontend/src/App.vue` - Add router-view with layout
- `frontend/src/main.ts` - Register router plugin + Element Plus + Icons
- `frontend/package.json` - Add Element Plus dependencies

---

## Task 1: Configure Element Plus

**Files:**
- Modify: `frontend/src/main.ts`
- Modify: `frontend/tests/setup.ts`

**Note:** Element Plus and icons are already installed in package.json. This task configures them in main.ts.

- [ ] **Step 1: Verify Element Plus is installed**

Run: `cd frontend && npm list element-plus @element-plus/icons-vue`
Expected: Shows element-plus@2.13.6 and @element-plus/icons-vue@2.3.2 installed

- [ ] **Step 2: Configure Element Plus in main.ts**

Modify `frontend/src/main.ts`:

```typescript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(ElementPlus, { locale: zhCn })

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app')
```

- [ ] **Step 3: Update tests/setup.ts for Element Plus components**

Modify `frontend/tests/setup.ts`:

```typescript
import { config } from '@vue/test-utils'
import ElementPlus from 'element-plus'

// Mock window.matchMedia for Element Plus
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {}, // deprecated
    removeListener: () => {}, // deprecated
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => false,
  }),
})

// Configure Vue Test Utils global settings
config.global.stubs = {
  teleport: true
}

// Register Element Plus globally for all tests
config.global.plugins = [ElementPlus]
```

- [ ] **Step 4: Verify Element Plus works**

Run: `cd frontend && npm run dev`
Expected: Dev server starts without errors

- [ ] **Step 5: Commit**

```bash
git add frontend/src/main.ts frontend/tests/setup.ts
git commit -m "feat: configure Element Plus with zh-CN locale and test setup"
```

---

## Task 2: Setup Vue Router

**Files:**
- Create: `frontend/src/router/index.ts`
- Modify: `frontend/src/main.ts:1-22`

**Note:** Vue Router is already installed in package.json. This task creates the router configuration.

- [ ] **Step 1: Write router configuration**

Create `frontend/src/router/index.ts`:

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
    component: () => import('@/views/Dashboard.vue'),
    meta: { title: '仪表盘' }
  },
  {
    path: '/strategies',
    name: 'StrategyList',
    component: () => import('@/views/StrategyList.vue'),
    meta: { title: '策略列表' }
  },
  {
    path: '/strategies/new',
    name: 'StrategyNew',
    component: () => import('@/views/StrategyEditor.vue'),
    meta: { title: '新建策略' }
  },
  {
    path: '/strategies/:id/edit',
    name: 'StrategyEdit',
    component: () => import('@/views/StrategyEditor.vue'),
    meta: { title: '编辑策略' }
  },
  {
    path: '/backtest/config',
    name: 'BacktestConfig',
    component: () => import('@/views/BacktestConfig.vue'),
    meta: { title: '回测配置' }
  },
  {
    path: '/backtest/:id',
    name: 'BacktestResult',
    component: () => import('@/views/BacktestResult.vue'),
    meta: { title: '回测结果' }
  },
  {
    path: '/optimize',
    name: 'Optimizer',
    component: () => import('@/views/Optimizer.vue'),
    meta: { title: '参数优化' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
```

- [ ] **Step 2: Register router in main.ts**

Modify `frontend/src/main.ts`:

```typescript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus, { locale: zhCn })

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app')
```

- [ ] **Step 3: Verify router works**

Run: `cd frontend && npm run dev`
Expected: Dev server starts without errors

- [ ] **Step 4: Commit**

```bash
git add frontend/src/router/index.ts frontend/src/main.ts
git commit -m "feat: add vue router with 7 routes per spec"
```

---

## Task 3: Header Component

**Files:**
- Create: `frontend/src/components/layout/Header.vue`
- Create: `frontend/tests/unit/components/layout/Header.test.ts`

- [ ] **Step 1: Write the failing test**

Create `frontend/tests/unit/components/layout/Header.test.ts`:

```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import Header from '@/components/layout/Header.vue'

describe('Header', () => {
  it('renders app title', () => {
    render(Header)
    expect(screen.getByText('AI Quant Platform')).toBeInTheDocument()
  })

  it('renders with el-header structure', () => {
    const { container } = render(Header)
    expect(container.querySelector('.el-header')).toBeInTheDocument()
  })

  it('has correct height from spec (60px)', () => {
    const { container } = render(Header)
    const header = container.querySelector('.el-header')
    expect(header).toHaveStyle({ height: '60px' })
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd frontend && npm run test -- tests/unit/components/layout/Header.test.ts`
Expected: FAIL with "Cannot find module '@/components/layout/Header.vue'"

- [ ] **Step 3: Write minimal implementation**

Create `frontend/src/components/layout/Header.vue`:

```vue
<template>
  <el-header :height="'60px'" class="app-header">
    <div class="header-content">
      <div class="logo-section">
        <h1 class="app-title">AI Quant Platform</h1>
      </div>
      <div class="header-actions">
        <!-- Placeholder for future user menu -->
      </div>
    </div>
  </el-header>
</template>

<script setup lang="ts">
// No logic needed yet
</script>

<style scoped>
.app-header {
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  padding: 0;
}

.header-content {
  height: 100%;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}
</style>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd frontend && npm run test -- tests/unit/components/layout/Header.test.ts`
Expected: PASS (all 3 tests pass)

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/layout/Header.vue frontend/tests/unit/components/layout/Header.test.ts
git commit -m "feat: add Header component with Element Plus (60px height)"
```

---

## Task 4: Sidebar Component

**Files:**
- Create: `frontend/src/components/layout/Sidebar.vue`
- Create: `frontend/tests/unit/components/layout/Sidebar.test.ts`

- [ ] **Step 1: Write the failing test**

Create `frontend/tests/unit/components/layout/Sidebar.test.ts`:

```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import { createRouter, createMemoryHistory } from 'vue-router'
import Sidebar from '@/components/layout/Sidebar.vue'

const routes = [
  { path: '/dashboard', name: 'Dashboard', component: { template: '<div>Dashboard</div>' } },
  { path: '/strategies', name: 'StrategyList', component: { template: '<div>Strategies</div>' } },
  { path: '/backtest/config', name: 'BacktestConfig', component: { template: '<div>Backtest</div>' } },
  { path: '/optimize', name: 'Optimizer', component: { template: '<div>Optimize</div>' } }
]

describe('Sidebar', () => {
  const createTestRouter = () => {
    return createRouter({
      history: createMemoryHistory(),
      routes
    })
  }

  it('renders exactly 4 navigation items per spec', async () => {
    const router = createTestRouter()
    render(Sidebar, {
      global: {
        plugins: [router]
      }
    })

    expect(screen.getByText('仪表盘')).toBeInTheDocument()
    expect(screen.getByText('策略管理')).toBeInTheDocument()
    expect(screen.getByText('回测配置')).toBeInTheDocument()
    expect(screen.getByText('参数优化')).toBeInTheDocument()
  })

  it('renders with el-aside and el-menu structure', () => {
    const router = createTestRouter()
    const { container } = render(Sidebar, {
      global: {
        plugins: [router]
      }
    })
    expect(container.querySelector('.el-aside')).toBeInTheDocument()
    expect(container.querySelector('.el-menu')).toBeInTheDocument()
  })

  it('has correct width from spec (200px)', () => {
    const router = createTestRouter()
    const { container } = render(Sidebar, {
      global: {
        plugins: [router]
      }
    })
    const aside = container.querySelector('.el-aside')
    expect(aside).toHaveAttribute('style', expect.stringContaining('width: 200px'))
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd frontend && npm run test -- tests/unit/components/layout/Sidebar.test.ts`
Expected: FAIL with "Cannot find module '@/components/layout/Sidebar.vue'"

- [ ] **Step 3: Write minimal implementation**

Create `frontend/src/components/layout/Sidebar.vue`:

```vue
<template>
  <el-aside width="200px" class="app-sidebar">
    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      @select="handleSelect"
    >
      <el-menu-item index="/dashboard">
        <span>📊</span>
        <span>仪表盘</span>
      </el-menu-item>
      <el-menu-item index="/strategies">
        <span>📝</span>
        <span>策略管理</span>
      </el-menu-item>
      <el-menu-item index="/backtest/config">
        <span>⚙️</span>
        <span>回测配置</span>
      </el-menu-item>
      <el-menu-item index="/optimize">
        <span>📈</span>
        <span>参数优化</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const activeMenu = computed(() => {
  return route.path
})

const handleSelect = (index: string) => {
  router.push(index)
}
</script>

<style scoped>
.app-sidebar {
  background-color: #ffffff;
  border-right: 1px solid #e5e7eb;
  height: 100%;
  overflow-y: auto;
}

.sidebar-menu {
  border-right: none;
  height: 100%;
}

.sidebar-menu .el-menu-item {
  height: 56px;
  line-height: 56px;
  padding-left: 24px;
}

.sidebar-menu .el-menu-item span:first-child {
  margin-right: 12px;
  font-size: 18px;
}
</style>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd frontend && npm run test -- tests/unit/components/layout/Sidebar.test.ts`
Expected: PASS (all 3 tests pass)

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/layout/Sidebar.vue frontend/tests/unit/components/layout/Sidebar.test.ts
git commit -m "feat: add Sidebar with 4 menu items using Element Plus el-menu"
```

---

## Task 5: AppLayout Component

**Files:**
- Create: `frontend/src/components/layout/AppLayout.vue`
- Create: `frontend/tests/unit/components/layout/AppLayout.test.ts`

- [ ] **Step 1: Write the failing test**

Create `frontend/tests/unit/components/layout/AppLayout.test.ts`:

```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import { createRouter, createMemoryHistory } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'

describe('AppLayout', () => {
  const createTestRouter = () => {
    return createRouter({
      history: createMemoryHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } }
      ]
    })
  }

  it('renders header component', () => {
    const router = createTestRouter()
    render(AppLayout, {
      global: {
        plugins: [router]
      }
    })
    expect(screen.getByText('AI Quant Platform')).toBeInTheDocument()
  })

  it('renders sidebar component', () => {
    const router = createTestRouter()
    render(AppLayout, {
      global: {
        plugins: [router]
      }
    })
    expect(screen.getByText('仪表盘')).toBeInTheDocument()
    expect(screen.getByText('策略管理')).toBeInTheDocument()
  })

  it('renders slot content in main area', () => {
    const router = createTestRouter()
    render(AppLayout, {
      slots: {
        default: '<div data-testid="main-content">Test Content</div>'
      },
      global: {
        plugins: [router]
      }
    })
    expect(screen.getByTestId('main-content')).toBeInTheDocument()
    expect(screen.getByText('Test Content')).toBeInTheDocument()
  })

  it('uses Element Plus el-container structure', () => {
    const router = createTestRouter()
    const { container } = render(AppLayout, {
      global: {
        plugins: [router]
      }
    })
    expect(container.querySelector('.el-container')).toBeInTheDocument()
    expect(container.querySelector('.el-header')).toBeInTheDocument()
    expect(container.querySelector('.el-aside')).toBeInTheDocument()
    expect(container.querySelector('.el-main')).toBeInTheDocument()
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd frontend && npm run test -- tests/unit/components/layout/AppLayout.test.ts`
Expected: FAIL with "Cannot find module '@/components/layout/AppLayout.vue'"

- [ ] **Step 3: Write minimal implementation**

Create `frontend/src/components/layout/AppLayout.vue`:

```vue
<template>
  <el-container class="app-layout">
    <Header />
    <el-container class="main-layout">
      <Sidebar />
      <el-main class="main-content">
        <slot></slot>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import Header from './Header.vue'
import Sidebar from './Sidebar.vue'
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  flex-direction: column;
}

.main-layout {
  flex: 1;
  overflow: hidden;
}

.main-content {
  background-color: #f9fafb;
  overflow-y: auto;
  padding: 24px;
}
</style>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd frontend && npm run test -- tests/unit/components/layout/AppLayout.test.ts`
Expected: PASS (all 4 tests pass)

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/layout/AppLayout.vue frontend/tests/unit/components/layout/AppLayout.test.ts
git commit -m "feat: add AppLayout with Element Plus el-container"
```

---

## Task 6: Dashboard View (Part 1 - Structure and Stats)

**Files:**
- Create: `frontend/src/views/Dashboard.vue`
- Create: `frontend/tests/unit/views/Dashboard.test.ts`

- [ ] **Step 1: Write the failing test**

Create `frontend/tests/unit/views/Dashboard.test.ts`:

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/vue'
import { createPinia, setActivePinia } from 'pinia'
import Dashboard from '@/views/Dashboard.vue'

describe('Dashboard', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders page title "工作台"', () => {
    render(Dashboard)
    expect(screen.getByText('工作台')).toBeInTheDocument()
  })

  it('renders four stat cards per spec', () => {
    render(Dashboard)
    expect(screen.getByText('策略总数')).toBeInTheDocument()
    expect(screen.getByText('运行中')).toBeInTheDocument()
    expect(screen.getByText('近30天收益')).toBeInTheDocument()
    expect(screen.getByText('夏普比率')).toBeInTheDocument()
  })

  it('displays placeholder values initially', () => {
    render(Dashboard)
    const values = screen.getAllByText('--')
    expect(values.length).toBeGreaterThan(0)
  })

  it('renders quick actions section', () => {
    render(Dashboard)
    expect(screen.getByText('快速操作')).toBeInTheDocument()
  })

  it('renders recent backtest section', () => {
    render(Dashboard)
    expect(screen.getByText('最近回测')).toBeInTheDocument()
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd frontend && npm run test -- tests/unit/views/Dashboard.test.ts`
Expected: FAIL with "Cannot find module '@/views/Dashboard.vue'"

- [ ] **Step 3: Write minimal implementation**

Create `frontend/src/views/Dashboard.vue`:

```vue
<template>
  <div class="dashboard">
    <div class="page-header">
      <h1 class="page-title">工作台</h1>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-label">策略总数</div>
        <div class="stat-value">{{ stats.totalStrategies }}</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon">⚡</div>
        <div class="stat-label">运行中</div>
        <div class="stat-value">{{ stats.running }}</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-label">近30天收益</div>
        <div class="stat-value">{{ stats.return30d }}</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon">📈</div>
        <div class="stat-label">夏普比率</div>
        <div class="stat-value">{{ stats.sharpeRatio }}</div>
      </el-card>
    </div>

    <!-- Quick Actions -->
    <el-card class="section-card">
      <template #header>
        <div class="section-title">快速操作</div>
      </template>
      <div class="quick-actions">
        <el-button type="primary" size="large">
          📝 新建策略
        </el-button>
        <el-button type="success" size="large">
          ⚡ 快速回测
        </el-button>
        <el-button type="info" size="large">
          📊 查看报告
        </el-button>
      </div>
    </el-card>

    <!-- Recent Backtests -->
    <el-card class="section-card">
      <template #header>
        <div class="section-title">最近回测</div>
      </template>
      <el-table :data="recentBacktests" style="width: 100%">
        <el-table-column prop="backtest_id" label="回测ID" width="120" />
        <el-table-column prop="strategy_name" label="策略名称" width="150" />
        <el-table-column prop="return" label="收益率" width="120" />
        <el-table-column prop="sharpe" label="夏普" width="100" />
        <el-table-column prop="drawdown" label="回撤" width="120" />
        <el-table-column prop="created_at" label="时间" width="150" />
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd frontend && npm run test -- tests/unit/views/Dashboard.test.ts`
Expected: PASS (all 5 tests pass)

- [ ] **Step 5: Commit**

```bash
git add frontend/src/views/Dashboard.vue frontend/tests/unit/views/Dashboard.test.ts
git commit -m "feat: add Dashboard view with 4 stats + quick actions + recent backtest table"
```

---

## Task 7: Integrate Layout with App.vue

**Files:**
- Modify: `frontend/src/App.vue`

- [ ] **Step 1: Read current App.vue**

Run: Read `frontend/src/App.vue`
Expected: See current structure (simple placeholder with "AI Quant Platform" heading)

- [ ] **Step 2: Replace App.vue content completely**

Replace the entire contents of `frontend/src/App.vue` with:

```vue
<template>
  <AppLayout>
    <router-view />
  </AppLayout>
</template>

<script setup lang="ts">
import AppLayout from '@/components/layout/AppLayout.vue'
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  width: 100%;
  min-height: 100vh;
}
</style>
```

- [ ] **Step 3: Verify in browser**

Run: `cd frontend && npm run dev`
Open: http://localhost:5173/
Expected: See header (60px), sidebar (200px), and dashboard page rendered correctly with Element Plus styling

- [ ] **Step 4: Test navigation**

In browser:
- Click "策略管理" in sidebar
Expected: Route changes to /strategies (shows blank page - component not created yet)
- Click "仪表盘" in sidebar
Expected: Route changes to /dashboard and dashboard displays

- [ ] **Step 5: Test root redirect**

In browser, navigate to: http://localhost:5173/
Expected: Automatically redirects to /dashboard

- [ ] **Step 6: Run all tests**

Run: `cd frontend && npm run test`
Expected: All new tests pass (12+ tests total)

- [ ] **Step 7: Commit**

```bash
git add frontend/src/App.vue
git commit -m "feat: integrate AppLayout and router-view in App.vue"
```

---

## Task 8: Create Placeholder View Components

**Files:**
- Create: `frontend/src/views/StrategyList.vue`
- Create: `frontend/src/views/StrategyEditor.vue`
- Create: `frontend/src/views/BacktestConfig.vue`
- Create: `frontend/src/views/BacktestResult.vue`
- Create: `frontend/src/views/Optimizer.vue`
- Create: `frontend/tests/unit/views/StrategyList.test.ts`
- Create: `frontend/tests/unit/views/StrategyEditor.test.ts`
- Create: `frontend/tests/unit/views/BacktestConfig.test.ts`
- Create: `frontend/tests/unit/views/BacktestResult.test.ts`
- Create: `frontend/tests/unit/views/Optimizer.test.ts`

**Note:** All 5 placeholder views follow the same pattern: el-card with title + description. Tests are written first (TDD), then implementations.

- [ ] **Step 1: Write all placeholder view tests**

Create test files for all 5 placeholder views. Each test checks for page title and placeholder message.

Create `frontend/tests/unit/views/StrategyList.test.ts`:
```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import StrategyList from '@/views/StrategyList.vue'

describe('StrategyList', () => {
  it('renders page title', () => {
    render(StrategyList)
    expect(screen.getByText('策略管理')).toBeInTheDocument()
  })

  it('renders placeholder message', () => {
    render(StrategyList)
    expect(screen.getByText(/即将推出/)).toBeInTheDocument()
  })
})
```

Create `frontend/tests/unit/views/StrategyEditor.test.ts`:
```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import StrategyEditor from '@/views/StrategyEditor.vue'

describe('StrategyEditor', () => {
  it('renders page title', () => {
    render(StrategyEditor)
    expect(screen.getByText('策略编辑器')).toBeInTheDocument()
  })

  it('renders placeholder message', () => {
    render(StrategyEditor)
    expect(screen.getByText(/即将推出/)).toBeInTheDocument()
  })
})
```

Create `frontend/tests/unit/views/BacktestConfig.test.ts`:
```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import BacktestConfig from '@/views/BacktestConfig.vue'

describe('BacktestConfig', () => {
  it('renders page title', () => {
    render(BacktestConfig)
    expect(screen.getByText('回测配置')).toBeInTheDocument()
  })

  it('renders placeholder message', () => {
    render(BacktestConfig)
    expect(screen.getByText(/即将推出/)).toBeInTheDocument()
  })
})
```

Create `frontend/tests/unit/views/BacktestResult.test.ts`:
```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import BacktestResult from '@/views/BacktestResult.vue'

describe('BacktestResult', () => {
  it('renders page title', () => {
    render(BacktestResult)
    expect(screen.getByText('回测结果')).toBeInTheDocument()
  })

  it('renders placeholder message', () => {
    render(BacktestResult)
    expect(screen.getByText(/即将推出/)).toBeInTheDocument()
  })
})
```

Create `frontend/tests/unit/views/Optimizer.test.ts`:
```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import Optimizer from '@/views/Optimizer.vue'

describe('Optimizer', () => {
  it('renders page title', () => {
    render(Optimizer)
    expect(screen.getByText('参数优化')).toBeInTheDocument()
  })

  it('renders placeholder message', () => {
    render(Optimizer)
    expect(screen.getByText(/即将推出/)).toBeInTheDocument()
  })
})
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd frontend && npm run test -- tests/unit/views/`
Expected: All 10 tests fail with "Cannot find module" errors

- [ ] **Step 3: Create StrategyList placeholder (2 min)**

Create `frontend/src/views/StrategyList.vue`:
```vue
<template>
  <div class="page-placeholder">
    <el-card>
      <h1 class="page-title">策略管理</h1>
      <p class="page-description">策略列表、编辑、删除功能即将推出</p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
// Placeholder component
</script>

<style scoped>
.page-placeholder {
  padding: 40px;
  text-align: center;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}

.page-description {
  font-size: 16px;
  color: #6b7280;
}
</style>
```

- [ ] **Step 4: Create StrategyEditor placeholder (2 min)**

Create `frontend/src/views/StrategyEditor.vue`:
```vue
<template>
  <div class="page-placeholder">
    <el-card>
      <h1 class="page-title">策略编辑器</h1>
      <p class="page-description">Monaco 编辑器集成功能即将推出</p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
// Placeholder component
</script>

<style scoped>
.page-placeholder {
  padding: 40px;
  text-align: center;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}

.page-description {
  font-size: 16px;
  color: #6b7280;
}
</style>
```

- [ ] **Step 5: Create BacktestConfig placeholder (2 min)**

Create `frontend/src/views/BacktestConfig.vue`:
```vue
<template>
  <div class="page-placeholder">
    <el-card>
      <h1 class="page-title">回测配置</h1>
      <p class="page-description">回测参数配置、执行功能即将推出</p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
// Placeholder component
</script>

<style scoped>
.page-placeholder {
  padding: 40px;
  text-align: center;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}

.page-description {
  font-size: 16px;
  color: #6b7280;
}
</style>
```

- [ ] **Step 6: Create BacktestResult placeholder (2 min)**

Create `frontend/src/views/BacktestResult.vue`:
```vue
<template>
  <div class="page-placeholder">
    <el-card>
      <h1 class="page-title">回测结果</h1>
      <p class="page-description">回测结果展示、图表、分析功能即将推出</p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
// Placeholder component
</script>

<style scoped>
.page-placeholder {
  padding: 40px;
  text-align: center;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}

.page-description {
  font-size: 16px;
  color: #6b7280;
}
</style>
```

- [ ] **Step 7: Create Optimizer placeholder (2 min)**

Create `frontend/src/views/Optimizer.vue`:
```vue
<template>
  <div class="page-placeholder">
    <el-card>
      <h1 class="page-title">参数优化</h1>
      <p class="page-description">参数扫描、优化、结果展示功能即将推出</p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
// Placeholder component
</script>

<style scoped>
.page-placeholder {
  padding: 40px;
  text-align: center;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}

.page-description {
  font-size: 16px;
  color: #6b7280;
}
</style>
```

- [ ] **Step 8: Run all tests to verify they pass**

Run: `cd frontend && npm run test -- tests/unit/views/`
Expected: All 10 view tests pass (Dashboard + 5 placeholders, 2 tests each)

- [ ] **Step 9: Test navigation in browser**

Run: `cd frontend && npm run dev`

In browser, test each route:
- http://localhost:5173/ → redirects to /dashboard
- /dashboard → Dashboard with stats cards
- /strategies → StrategyList placeholder
- /strategies/new → StrategyEditor placeholder
- /backtest/config → BacktestConfig placeholder
- /optimize → Optimizer placeholder

Expected: All routes work, sidebar highlights active item, Element Plus styling applied

- [ ] **Step 10: Commit**

```bash
git add frontend/src/views/*.vue frontend/tests/unit/views/*.test.ts
git commit -m "feat: add 5 placeholder views with tests (TDD workflow)"
```

---

## Task 9: Final Verification

**Files:**
- None (verification only)

- [ ] **Step 1: Run all tests**

Run: `cd frontend && npm run test`
Expected: All tests pass (22+ passing tests)

- [ ] **Step 2: Run linter**

Run: `cd frontend && npm run lint`
Expected: No linting errors

- [ ] **Step 3: Build production bundle**

Run: `cd frontend && npm run build`
Expected: Build succeeds without errors

- [ ] **Step 4: Manual browser testing checklist**

Run: `cd frontend && npm run dev`
Test checklist:
- [ ] Header displays "AI Quant Platform" with 60px height
- [ ] Sidebar shows exactly 4 navigation items (仪表盘, 策略管理, 回测配置, 参数优化)
- [ ] Sidebar width is 200px per spec
- [ ] Clicking sidebar items navigates to correct routes
- [ ] Active route is highlighted in sidebar (Element Plus el-menu styling)
- [ ] Dashboard shows "工作台" title
- [ ] Dashboard shows 4 stat cards: 策略总数, 运行中, 近30天收益, 夏普比率
- [ ] Dashboard shows quick actions section with 3 buttons
- [ ] Dashboard shows recent backtest table (empty initially)
- [ ] All placeholder pages display correctly with el-card styling
- [ ] Root path (/) redirects to /dashboard
- [ ] Element Plus Chinese locale works correctly

- [ ] **Step 5: Final commit and summary**

Create git tag:
```bash
git tag -a v0.1.0-layout-dashboard -m "Layout and Dashboard milestone complete per spec"
```

**Summary:**
- ✅ Element Plus installed and configured with zh-CN locale
- ✅ Vue Router configured with 7 routes (including redirect from /)
- ✅ Header component (60px, Element Plus el-header)
- ✅ Sidebar component (200px, 4 menu items, Element Plus el-menu)
- ✅ AppLayout component (Element Plus el-container structure)
- ✅ Dashboard view (4 stats + quick actions + recent backtest table)
- ✅ 5 placeholder views (StrategyList, StrategyEditor, BacktestConfig, BacktestResult, Optimizer)
- ✅ All components tested (22+ tests)
- ✅ Navigation working correctly
- ✅ Fully aligned with spec `/Users/maofengning/work/project/aicoding/ai-quant/docs/superpowers/specs/2026-03-23-frontend-ui-design.md`
- ✅ Ready for next phase: Data fetching and individual page implementations

---

## Next Steps

After completing this plan, the following features are ready to build (each should be a separate plan):

1. **Strategy List Page** - Implement strategy CRUD operations, table with filters
2. **Strategy Editor Page** - Integrate Monaco editor for Python strategy code
3. **Backtest Config Page** - Build form for backtest parameters with validation
4. **Backtest Result Page** - Add charts (ECharts), tabs, metrics display
5. **Parameter Optimization Page** - Implement parameter grid, progress tracking, results table

Each of these should reference the spec sections and be implemented with TDD workflow.
