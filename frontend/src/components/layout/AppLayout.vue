<template>
  <el-container class="app-layout">
    <Header />
    <el-container class="main-layout">
      <Sidebar />
      <el-main class="main-content">
        <router-view />
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