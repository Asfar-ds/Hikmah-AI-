// import { defineConfig } from "vite";
// import react from "@vitejs/plugin-react";
// import tailwindcss from "@tailwindcss/vite"

// export default defineConfig({
//   plugins: [react(),
//     tailwindcss()
//   ],

//   // server: {
//   //   proxy: {
//   //     "/voice-to-text": "http://localhost:8000",
//   //     "/text-to-voice": "http://localhost:8000",
//   //   },
//   // },
// });

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from "@tailwindcss/vite"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(),
    tailwindcss()
  ],
  server: {
    proxy: {
      // Proxy requests from /api to your backend server
      '/api': {
        target: 'http://localhost:8000', // The address of your backend (FastAPI, etc.)
        changeOrigin: true, // Needed for virtual hosting
        secure: false, // Set to true if your backend uses HTTPS
        rewrite: (path) => path.replace(/^\/api/, '') // You might need this if your backend expects /chat instead of /api/chat
      }
    }
  }
});