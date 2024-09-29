<script lang="ts">
	import Dashboard from '../../../utils/dashboard/Dashboard.svelte';
	import Footer from '../../Footer.svelte';
	import type { PageData } from './$types';
	export let data: PageData;
	
</script>

<main class="p-4">
	<Dashboard {data} />
</main>
<Footer />