<template>
  <div class="strategy-list">
    <div class="page-header">
      <h1 class="page-title">
        策略管理
      </h1>
      <el-button
        type="primary"
        @click="handleCreate"
      >
        新建策略
      </el-button>
    </div>

    <el-card>
      <el-table
        v-loading="loading"
        :data="strategies"
        style="width: 100%"
      >
        <el-table-column
          prop="name"
          label="策略名称"
          min-width="150"
        />
        <el-table-column
          prop="strategy_id"
          label="策略ID"
          width="200"
        />
        <el-table-column
          prop="created_at"
          label="创建时间"
          width="180"
        >
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column
          prop="updated_at"
          label="更新时间"
          width="180"
        >
          <template #default="{ row }">
            {{ formatDate(row.updated_at) }}
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="200"
          fixed="right"
        >
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty
        v-if="!loading && strategies.length === 0"
        description="暂无策略，请创建第一个策略"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { strategyApi } from '@/api/strategy'
import type { Strategy } from '@/types/api'

const router = useRouter()

const loading = ref(false)
const strategies = ref<Strategy[]>([])

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

const formatDate = (dateStr: string) => {
  if (!dateStr) return '--'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handleCreate = () => {
  router.push('/strategies/new')
}

const handleEdit = (row: Strategy) => {
  router.push(`/strategies/${row.strategy_id}/edit`)
}

const handleDelete = async (row: Strategy) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除策略 "${row.name}" 吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await strategyApi.delete(row.strategy_id)
    ElMessage.success('删除成功')
    fetchStrategies()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchStrategies()
})
</script>

<style scoped>
.strategy-list {
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}
</style>