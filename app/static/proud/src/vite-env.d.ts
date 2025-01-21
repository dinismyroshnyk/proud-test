// <reference types="svelte" />
// <reference types="vite/client" />

declare module '*.svelte' {
    import type { SvelteComponent } from 'svelte';
    const component: SvelteComponent;
    export default component;
}