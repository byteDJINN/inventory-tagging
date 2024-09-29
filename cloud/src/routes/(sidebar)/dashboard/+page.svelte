<script lang="ts">
	import Dashboard from '../../utils/dashboard/Dashboard.svelte';
	import Footer from '../Footer.svelte';
	export let data;
</script>


<main class="p-4">
	<Dashboard {data} />
</main>
<Footer />