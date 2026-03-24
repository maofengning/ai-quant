import { config } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import '@testing-library/jest-dom'

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

// Register Element Plus globally for all tests
config.global.plugins = [ElementPlus]
