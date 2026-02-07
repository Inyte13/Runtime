module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true
  },
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: { jsx: true },
    sourceType: 'module'
  },
  plugins: ['@typescript-eslint', 'react-hooks'],
  extends: [
    'eslint:recommended',
    'standard',
    'plugin:@typescript-eslint/recommended'
  ],
  rules: {
    // TS manda
    'no-unused-vars': 'off',
    '@typescript-eslint/no-unused-vars': 'warn'
  }
}
