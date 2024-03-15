import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwind from "@astrojs/tailwind";

import vue from "@astrojs/vue";

// https://astro.build/config
export default defineConfig({
    outDir: '../../dist/astro',
    site: "http://127.0.0.1:5000",
    integrations: [
        tailwind(),
        vue({ appEntrypoint: '/src/Application' }),
        mdx(),
        sitemap()
    ]
});
