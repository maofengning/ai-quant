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
        row-key="strategy_id"
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
          width="240"
          fixed="right"
        >
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click.stop="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              type="success"
              size="small"
              @click.stop="handleBacktest(row)"
            >
              回测
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click.stop="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>

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
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchStrategies = async () => {
  loading.value = true
  try {
    const response = await strategyApi.getList({
      page: currentPage.value,
      page_size: pageSize.value
    })
    strategies.value = response.strategies
    total.value = response.strategies.length
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

const handleBacktest = (row: Strategy) => {
  router.push({ path: '/backtest/config', query: { strategyId: row.strategy_id } })
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

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchStrategies()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  fetchStrategies()
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

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>