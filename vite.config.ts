import fs from 'node:fs';
import path from 'node:path';
import { defineConfig, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

function syncDocsToDistPlugin(): Plugin {
  return {
    name: 'sync-docs-to-dist',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        if (req.url === '/docs') {
          res.writeHead(302, { Location: '/docs/index.html' });
          res.end();
          return;
        }
        next();
      });
    },
    closeBundle() {
      const rootDir = __dirname;
      const docsDir = path.join(rootDir, 'docs');
      const distDocsDir = path.join(rootDir, 'dist', 'docs');
      if (!fs.existsSync(docsDir) || !fs.existsSync(path.join(rootDir, 'dist'))) return;
      fs.mkdirSync(distDocsDir, { recursive: true });
      for (const entry of fs.readdirSync(docsDir)) {
        if (entry === 'explorer') continue;
        const src = path.join(docsDir, entry);
        const dst = path.join(distDocsDir, entry);
        const stat = fs.statSync(src);
        if (stat.isFile() && entry.endsWith('.html')) {
          fs.copyFileSync(src, dst);
        } else if (stat.isDirectory() && entry === 'assets') {
          fs.cpSync(src, dst, { recursive: true });
        }
      }
    },
  };
}

export default defineConfig({
  base: './',
  plugins: [react(), tailwindcss(), syncDocsToDistPlugin()],
  server: {
    port: 3000,
    host: '0.0.0.0',
    allowedHosts: true,
    hmr: process.env.DISABLE_HMR === 'true' ? false : undefined,
  },
});
