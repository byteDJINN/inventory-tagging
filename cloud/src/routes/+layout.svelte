<script>
	import modeobserver from './utils/modeobserver';
	import { onMount } from 'svelte';

  export let data;

	onMount(modeobserver);
</script>
<slot />
