import { createApp } from 'vue'
import App from './App.vue'

async function enableMocking() {
  if (import.meta.env.MODE === 'development') {
    const { worker } = await import('./mocks/browser')
    return worker.start({
      onUnhandledRequest: 'bypass'
    })
  }
}

enableMocking().then(() => {
  const app = createApp(App)
  app.mount('#app')
})
