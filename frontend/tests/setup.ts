import { config } from '@vue/test-utils'

// Mock window.matchMedia for Element Plus
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {}, // deprecated
    removeListener: () => {}, // deprecated
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => false,
  }),
})

// Configure Vue Test Utils global settings
config.global.stubs = {
  teleport: true
}
