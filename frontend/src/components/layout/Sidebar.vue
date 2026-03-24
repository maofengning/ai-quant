<template>
  <el-aside
    width="200px"
    class="app-sidebar"
  >
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