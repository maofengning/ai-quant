<template>
  <div
    ref="editorContainer"
    class="code-editor-container"
    :style="{ height: height }"
  />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, shallowRef } from 'vue'
import * as monaco from 'monaco-editor'
import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker'
import jsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker'
import cssWorker from 'monaco-editor/esm/vs/language/css/css.worker?worker'
import htmlWorker from 'monaco-editor/esm/vs/language/html/html.worker?worker'
import tsWorker from 'monaco-editor/esm/vs/language/typescript/ts.worker?worker'

// Configure Monaco workers
self.MonacoEnvironment = {
  getWorker(_, label) {
    if (label === 'json') {
      return new jsonWorker()
    }
    if (label === 'css' || label === 'scss' || label === 'less') {
      return new cssWorker()
    }
    if (label === 'html' || label === 'handlebars' || label === 'razor') {
      return new htmlWorker()
    }
    if (label === 'typescript' || label === 'javascript') {
      return new tsWorker()
    }
    return new editorWorker()
  }
}

interface Props {
  modelValue?: string
  language?: 'python' | 'javascript' | 'typescript' | 'json'
  readonly?: boolean
  height?: string
  theme?: 'vs' | 'vs-dark'
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  language: 'python',
  readonly: false,
  height: '400px',
  theme: 'vs'
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'validate': [isValid: boolean, errors: string[]]
}>()

const editorContainer = ref<HTMLElement>()
const editor = shallowRef<monaco.editor.IStandaloneCodeEditor | null>(null)

// Initialize editor
onMounted(() => {
  if (!editorContainer.value) return

  editor.value = monaco.editor.create(editorContainer.value, {
    value: props.modelValue,
    language: props.language,
    theme: props.theme,
    readOnly: props.readonly,
    minimap: { enabled: false },
    fontSize: 14,
    lineNumbers: 'on',
    scrollBeyondLastLine: false,
    automaticLayout: true,
    tabSize: 4,
    insertSpaces: true,
    wordWrap: 'on',
    padding: { top: 12, bottom: 12 },
    scrollbar: {
      verticalScrollbarSize: 10,
      horizontalScrollbarSize: 10
    },
    renderLineHighlight: 'line',
    folding: true,
    lineDecorationsWidth: 10,
    lineNumbersMinChars: 3
  })

  // Listen for content changes
  editor.value.onDidChangeModelContent(() => {
    const value = editor.value?.getValue() || ''
    emit('update:modelValue', value)
  })
})

// Watch for external value changes
watch(() => props.modelValue, (newValue) => {
  if (editor.value && newValue !== editor.value.getValue()) {
    editor.value.setValue(newValue)
  }
})

// Watch for language changes
watch(() => props.language, (newLanguage) => {
  if (editor.value) {
    const model = editor.value.getModel()
    if (model) {
      monaco.editor.setModelLanguage(model, newLanguage)
    }
  }
})

// Watch for readonly changes
watch(() => props.readonly, (readonly) => {
  editor.value?.updateOptions({ readOnly: readonly })
})

// Cleanup
onUnmounted(() => {
  editor.value?.dispose()
})

// Expose methods
defineExpose({
  getEditor: () => editor.value,
  focus: () => editor.value?.focus(),
  getValue: () => editor.value?.getValue() || '',
  setValue: (value: string) => editor.value?.setValue(value)
})
</script>

<style scoped>
.code-editor-container {
  width: 100%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}

.code-editor-container :deep(.monaco-editor) {
  border-radius: 4px;
}
</style>