import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import path from 'path';

export default {
    extensions: ['.svelte', '.ts'],
    preprocess: [
        vitePreprocess({
            typescript: true
        })
    ],
    kit: {
        vite: {
            resolve: {
                alias: {
                    $assets: path.resolve('src/assets')
                }
            }
        }
    }
};