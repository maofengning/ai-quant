<template>
  <el-header
    :height="'60px'"
    class="app-header"
  >
    <div class="header-content">
      <div class="logo-section">
        <h1 class="app-title">
          AI Quant Platform
        </h1>
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