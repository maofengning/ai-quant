module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
    'plugin:@typescript-eslint/recommended',
  ],
  parser: 'vue-eslint-parser',
  parserOptions: {
    ecmaVersion: 'latest',
    parser: '@typescript-eslint/parser',
    sourceType: 'module',
  },
  plugins: ['vue', '@typescript-eslint'],
  rules: {
    // Allow single word component names for common UI patterns
    'vue/multi-word-component-names': ['error', {
      ignores: ['Dashboard', 'Optimizer', 'Header', 'Sidebar', 'AppLayout']
    }],
    // Allow any type in tests
    '@typescript-eslint/no-explicit-any': 'off',
  },
}
