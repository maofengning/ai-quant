import { ref, onUnmounted } from 'vue'

export interface PollingOptions<T> {
  /** Polling interval in milliseconds */
  interval?: number
  /** Condition to stop polling - return false to stop */
  condition?: (data: T | null) => boolean
  /** Called on each poll */
  onPoll?: (data: T | null) => void
  /** Called on error */
  onError?: (error: Error) => void
}

export function usePolling<T>(
  fetchFn: () => Promise<T>,
  options: PollingOptions<T> = {}
) {
  const {
    interval = 2000,
    condition = () => true,
    onPoll,
    onError
  } = options

  const data = ref<T | null>(null)
  const isPolling = ref(false)
  const error = ref<Error | null>(null)
  const isComplete = ref(false)

  let pollTimer: ReturnType<typeof setInterval> | null = null

  const start = () => {
    if (isPolling.value) return

    isPolling.value = true
    isComplete.value = false
    error.value = null

    const poll = async () => {
      try {
        const result = await fetchFn()
        data.value = result

        onPoll?.(result)

        if (!condition(result)) {
          isComplete.value = true
          stop()
        }
      } catch (e) {
        error.value = e as Error
        onError?.(error.value)
      }
    }

    // Initial poll
    poll()

    // Start interval
    pollTimer = setInterval(poll, interval)
  }

  const stop = () => {
    if (pollTimer) {
      clearInterval(pollTimer)
      pollTimer = null
    }
    isPolling.value = false
  }

  const restart = () => {
    stop()
    start()
  }

  onUnmounted(() => {
    stop()
  })

  return {
    data,
    isPolling,
    error,
    isComplete,
    start,
    stop,
    restart
  }
}