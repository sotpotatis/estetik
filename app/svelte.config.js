import adapter from '@sveltejs/adapter-netlify';
import preprocess from 'svelte-preprocess';
/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter(),
		vite: {
			server:
				{
					fs: {
						allow: ['./static/'] // Allow static routes to be accessed
					}
				}
		},
		prerender: {
			default: true
		}
	},
	preprocess: [
		preprocess({
			postcss: true
		})
	]
};

export default config;
