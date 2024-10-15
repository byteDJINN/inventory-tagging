<script lang="ts">
	import Change from '../dashboard/Change.svelte';
	import type { ApexOptions } from 'apexcharts';
	import { Card, Chart, Heading } from 'flowbite-svelte';
	import LastRange from './LastRange.svelte';
	import More from './More.svelte';

	export let title: string = '';
	export let subtitle: string = '';
	export let chartOptions: ApexOptions;

	// Calculate the change percentage
	$: changePercentage = calculateChangePercentage(chartOptions);

	function calculateChangePercentage(options: ApexOptions): number {
		if (options.series && Array.isArray(options.series) && options.series.length > 0) {
			const data = options.series[0].data;
			if (Array.isArray(data) && data.length >= 2) {
				const currentValue = data[data.length - 1].y;
				const previousValue = data[data.length - 2].y;
				return ((currentValue - previousValue) / previousValue) * 100;
			}
		}
		return 0;
	}
</script>

<Card size="xl" class="w-full max-w-none 2xl:col-span-2">
	<div class="mb-4 flex items-center justify-between">
		<div class="flex-shrink-0">
			<Heading tag="h3" class="text-2xl">{title}</Heading>
			<p class="text-base font-light text-gray-500 dark:text-gray-400">{subtitle}</p>
		</div>
		<Change value={changePercentage} since="yesterday" class="justify-end font-medium" />
	</div>

	<Chart options={chartOptions}></Chart>

</Card>

<!--
@component
[Go to docs](https://flowbite-svelte-admin-dashboard.vercel.app/)
## Props
@prop export let title: string = '';
@prop export let subtitle: string = '';
@prop export let chartOptions: ApexOptions;
-->
