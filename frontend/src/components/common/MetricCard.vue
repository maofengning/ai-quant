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
