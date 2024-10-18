<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	onMount(() => {
		const unsubscribe = page.subscribe(($page) => {
			if (!$page.data.user && !$page.url.pathname.startsWith('/authentication')) {
				goto('/authentication/sign-in');
			}
		});

		return unsubscribe;
	});
</script>

<slot />
