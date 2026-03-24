// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: AppLayout,
    redirect: '/dashboard',
    children: [
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
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router