import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'
import path from 'node:path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/bloques': 'http://127.0.0.1:8000',
      '/dias': 'http://127.0.0.1:8000',
      '/configuracion': 'http://127.0.0.1:8000',
      '/actividades': 'http://127.0.0.1:8000',
    },
  },
})
