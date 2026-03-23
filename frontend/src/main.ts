import { createApp } from 'vue'
import App from './App.vue'
import pinia from './stores'

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
  app.use(pinia)
  app.mount('#app')
})
