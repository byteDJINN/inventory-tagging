<script lang="ts">
	import thickbars from '../graphs/thickbars';
	import ChartWidget from '../widgets/ChartWidget.svelte';
	import { Card, Chart } from 'flowbite-svelte';
	// import type { PageData } from '../../routes/(sidebar)/$types';
	import type { PageData } from '../../(sidebar)/$types';
	import Stats from './Stats.svelte';
	import { onMount } from 'svelte';

	// import chart_options_func from '../../routes/(sidebar)/dashboard/chart_options';
  import chart_options_func from '../../(sidebar)/dashboard/chart_options';
	import Change from './Change.svelte';

	export let data: PageData;

	let chartOptions = chart_options_func(false);
	chartOptions.series = data.series;

	let dark = false;

	function handler(ev: Event) {
		if ('detail' in ev) {
			chartOptions = chart_options_func(ev.detail);
			chartOptions.series = data.series;
			dark = !!ev.detail;
		}
	}
</script>

<div class="space-y-4">
	<div class="grid gap-4 xl:grid-cols-2 2xl:grid-cols-3">
		<ChartWidget {chartOptions} title="$45,385" subtitle="Sales this week" />

		<Stats />
	</div>
	<div class="grid grid-cols-1 gap-4 xl:grid-cols-2 2xl:grid-cols-3">
		<Card horizontal class="items-center justify-between" size="xl">
			<div class="w-full">
				<p>New products</p>
				<p class="text-2xl font-bold leading-none text-gray-900 dark:text-white sm:text-3xl">
					2,340
				</p>
				<Change size="sm" value={12.5} since="Since last month" />
			</div>
			<Chart options={thickbars} class="w-full" />
		</Card>

	</div>
</div>
