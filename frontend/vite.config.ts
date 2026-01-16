import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
    base:
        mode == "development"
            ? "http://localhost:5173/"
            : "/static/api/spa/",
    build: {
        emptyOutDir: true,
        outDir: "../api/static/api/spa",
    },
    plugins: [vue()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
    server: {
        proxy: {
            // Proxy API requests to Django backend with cookie forwarding
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                cookieDomainRewrite: 'localhost',
            },
            // Proxy media files to Django backend
            '/media': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
            // Proxy login/logout to Django backend
            '/login': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
            '/logout': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
            '/signup': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
        },
    },
}));
