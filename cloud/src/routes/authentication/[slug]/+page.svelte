<script lang="ts">
	import type { PageData } from './$types';
	export let data: PageData;
	console.log(data.params);
	
</script>

<svelte:component this={data.content} />
