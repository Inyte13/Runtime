import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/bloques': 'http://127.0.0.1:8000',
      '/dias': 'http://127.0.0.1:8000',
      '/configuracion': 'http://127.0.0.1:8000',
      '/actividades': 'http://127.0.0.1:8000'
    }
  }
})
