import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // this tells Vite: "If the React app calls /api, send it to the FastAPI container"
      '/api': {
        target: 'http://server:8000', // 'server' is docker-compose service name
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }  
})
