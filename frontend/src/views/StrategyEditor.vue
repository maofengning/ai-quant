<template>
  <div class="strategy-editor">
    <div class="page-header">
      <h1 class="page-title">
        {{ isEdit ? '编辑策略' : '新建策略' }}
      </h1>
      <div class="header-actions">
        <el-button @click="router.push('/strategies')">
          取消
        </el-button>
        <el-button
          type="primary"
          :loading="saving"
          @click="handleSave"
        >
          保存
        </el-button>
        <el-button
          type="success"
          :loading="running"
          @click="handleSaveAndBacktest"
        >
          保存并回测
        </el-button>
      </div>
    </div>

    <el-card>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item
          label="策略名称"
          prop="name"
        >
          <el-input
            v-model="form.name"
            placeholder="请输入策略名称"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>

        <el-form-item
          label="策略代码"
          prop="code"
        >
          <div class="editor-wrapper">
            <div class="editor-toolbar">
              <span class="toolbar-title">Python</span>
            </div>
            <CodeEditor
              v-model="form.code"
              language="python"
              height="500px"
            />
          </div>
          <div class="form-tip">
            提示: 策略需要实现 initialize() 和 on_bar() 方法
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { strategyApi } from '@/api/strategy'
import { backtestApi } from '@/api/backtest'
import CodeEditor from '@/components/editor/CodeEditor.vue'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()

const saving = ref(false)
const running = ref(false)
const loading = ref(false)

const isEdit = computed(() => !!route.params.id)
const strategyId = computed(() => route.params.id as string)

const defaultCode = `# 策略示例代码
from typing import Dict, Any

class MyStrategy:
    """简单移动平均线策略"""

    def __init__(self):
        self.short_window = 10
        self.long_window = 30
        self.positions = {}

    def initialize(self, context: Dict[str, Any]):
        """初始化策略参数"""
        self.short_window = context.get('short_window', 10)
        self.long_window = context.get('long_window', 30)

    def on_bar(self, bar):
        """每个交易日执行的策略逻辑"""
        symbol = bar.symbol

        # 获取历史数据
        history = self.get_bars(symbol, self.long_window)

        if len(history) < self.long_window:
            return

        # 计算移动平均线
        short_ma = history[-self.short_window:]['close'].mean()
        long_ma = history[-self.long_window:]['close'].mean()

        # 交易逻辑
        current_position = self.get_position(symbol)

        if short_ma > long_ma and current_position == 0:
            # 金叉，买入信号
            self.buy(symbol, bar.close, 100)
        elif short_ma < long_ma and current_position > 0:
            # 死叉，卖出信号
            self.sell(symbol, bar.close, 100)
`

const form = reactive({
  name: '',
  code: defaultCode
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入策略名称', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入策略代码', trigger: 'blur' }
  ]
}


const fetchStrategy = async () => {
  if (!isEdit.value) return

  loading.value = true
  try {
    const strategy = await strategyApi.getById(strategyId.value)
    form.name = strategy.name
    form.code = strategy.code
  } catch (error) {
    ElMessage.error('获取策略信息失败')
    router.push('/strategies')
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    saving.value = true
    try {
      if (isEdit.value) {
        await strategyApi.update(strategyId.value, {
          name: form.name,
          code: form.code
        })
        ElMessage.success('更新成功')
      } else {
        await strategyApi.create({
          name: form.name,
          code: form.code
        })
        ElMessage.success('创建成功')
      }
      router.push('/strategies')
    } catch (error) {
      ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    } finally {
      saving.value = false
    }
  })
}

const handleSaveAndBacktest = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    saving.value = true
    running.value = true
    try {
      let strategyIdValue = strategyId.value

      // Save strategy first
      if (isEdit.value) {
        await strategyApi.update(strategyIdValue, {
          name: form.name,
          code: form.code
        })
        ElMessage.success('更新成功')
      } else {
        const result = await strategyApi.create({
          name: form.name,
          code: form.code
        })
        strategyIdValue = result.strategy_id
        ElMessage.success('创建成功')
      }
      ElMessage.success('回测已启动')
      const response = await backtestApi.run({
        strategy_id: strategyIdValue,
        symbols: ['000001.SZ'],
        start_date: '2023-01-01',
        end_date: '2024-01-01',
        initial_capital: 100000,
        commission: 0.0003,
        slippage: 0.001
      })

      ElMessage.success('回测已启动')
      router.push(`/backtest/${response.backtest_id}`)
    } catch (error) {
      ElMessage.error(isEdit.value ? '更新失败或回测启动失败' : '创建失败或回测启动失败')
    } finally {
      saving.value = false
      running.value = false
    }
  })
}

onMounted(() => {
  fetchStrategy()
})
</script>

<style scoped>
.strategy-editor {
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

.header-actions {
  display: flex;
  gap: 12px;
}

.editor-wrapper {
  width: 100%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}

.editor-toolbar {
  background: #f5f7fa;
  padding: 8px 12px;
  border-bottom: 1px solid #dcdfe6;
}

.toolbar-title {
  font-size: 12px;
  color: #909399;
}

.form-tip {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 8px;
}
</style>