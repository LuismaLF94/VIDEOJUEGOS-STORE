import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Carga automáticamente las variables de entorno
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: process.env.VITE_API_URL || "http://127.0.0.1:5000",
        changeOrigin: true,
        secure: false,
      },
    },
  },
  define: {
    "import.meta.env.VITE_API_URL": JSON.stringify(process.env.VITE_API_URL),
  },
  build: {
    outDir: "../backend/static", // ⚡ esto asegura que el frontend se sirva desde Flask
    emptyOutDir: true,
  },
});
