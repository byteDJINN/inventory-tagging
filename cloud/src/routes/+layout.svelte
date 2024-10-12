<script>
	import { onMount } from 'svelte';
	import { checkAuth } from '$lib/auth';
	import { writable } from 'svelte/store';

	const isLoading = writable(true);

	onMount(async () => {
		await checkAuth();
		isLoading.set(false);
	});
</script>

{#if $isLoading}
<div></div>
{:else}
	<slot />
{/if}
