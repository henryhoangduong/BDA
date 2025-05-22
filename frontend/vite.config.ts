import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': '/src'
    }
  },
  server: {
    proxy: {
      '/pdf': {
        target: 'https://www.tutorialspoint.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/pdf/, '')
      }
    }
  }
})
