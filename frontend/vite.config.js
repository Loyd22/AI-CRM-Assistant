import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Vite must export a config object.
// This tells Vite: "use React plugin" and start the dev server normally.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // frontend default port
  },
});