import { ref, onUnmounted, type Ref } from 'vue'

export interface WebSocketOptions {
  url: string
  autoReconnect?: boolean
  reconnectInterval?: number
  heartbeatInterval?: number
}

export interface WebSocketMessage {
  type: string
  data?: unknown
}

export function useWebSocket(options: WebSocketOptions) {
  const {
    url,
    autoReconnect = true,
    reconnectInterval = 3000,
    heartbeatInterval = 30000
  } = options

  const socket: Ref<WebSocket | null> = ref(null)
  const isConnected = ref(false)
  const lastMessage = ref<WebSocketMessage | null>(null)
  const error = ref<Error | null>(null)

  let reconnectTimer: ReturnType<typeof setTimeout> | null = null
  let heartbeatTimer: ReturnType<typeof setInterval> | null = null

  const messageHandlers: Map<string, (data: unknown) => void> = new Map()

  const connect = (): Promise<void> => {
    return new Promise((resolve, reject) => {
      try {
        const ws = new WebSocket(url)

        ws.onopen = () => {
          isConnected.value = true
          error.value = null

          // Start heartbeat
          startHeartbeat()

          resolve()
        }

        ws.onerror = () => {
          error.value = new Error('WebSocket connection error')
          reject(error.value)
        }

        ws.onclose = () => {
          isConnected.value = false
          stopHeartbeat()

          if (autoReconnect) {
            scheduleReconnect()
          }
        }

        ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data)
            lastMessage.value = message

            // Handle registered message types
            if (messageHandlers.has(message.type)) {
              messageHandlers.get(message.type)?.(message.data)
            }
          } catch (e) {
            console.error('Failed to parse WebSocket message:', e)
          }
        }

        socket.value = ws
      } catch (e) {
        reject(e)
      }
    })
  }

  const disconnect = () => {
    stopHeartbeat()
    cancelReconnect()

    if (socket.value) {
      socket.value.close()
      socket.value = null
    }

    isConnected.value = false
  }

  const send = (message: WebSocketMessage) => {
    if (socket.value && socket.value.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify(message))
    }
  }

  const onMessage = (type: string, handler: (data: unknown) => void) => {
    messageHandlers.set(type, handler)
  }

  const offMessage = (type: string) => {
    messageHandlers.delete(type)
  }

  const scheduleReconnect = () => {
    if (reconnectTimer) return

    reconnectTimer = setTimeout(() => {
      reconnectTimer = null
      connect().catch(() => {
        // Will retry automatically
      })
    }, reconnectInterval)
  }

  const cancelReconnect = () => {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }
  }

  const startHeartbeat = () => {
    stopHeartbeat()
    heartbeatTimer = setInterval(() => {
      send({ type: 'ping' })
    }, heartbeatInterval)
  }

  const stopHeartbeat = () => {
    if (heartbeatTimer) {
      clearInterval(heartbeatTimer)
      heartbeatTimer = null
    }
  }

  onUnmounted(() => {
    disconnect()
  })

  return {
    socket,
    isConnected,
    lastMessage,
    error,
    connect,
    disconnect,
    send,
    onMessage,
    offMessage
  }
}