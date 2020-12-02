import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		// properties to pass on to App.svelte
		//name: 'world'
	}
});

export default app;
