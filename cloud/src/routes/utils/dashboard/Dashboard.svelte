<script lang="ts">
	import thickbars from '../graphs/thickbars';
	import ChartWidget from '../widgets/ChartWidget.svelte';
	import { Card, Chart } from 'flowbite-svelte';
	import type { PageData } from '../../(sidebar)/$types';
	import Stats from './Stats.svelte';
	import { onMount } from 'svelte';
	import chart_options_func from '../../(sidebar)/dashboard/chart_options';
	import Change from './Change.svelte';
	import { pb } from '$lib/pocketbase';

	export let data: PageData;

	let chartOptions = chart_options_func(false);
	let salesData = [];
	let totalSales = 0;

	onMount(async () => {
		try {
			const records = await pb.collection('items').getList(1, 50, {
				sort: '-timeSold',
				filter: 'timeSold != null'
			});

			const salesByDate = records.items.reduce((acc, item) => {
				const date = new Date(item.timeSold).toLocaleDateString('en-US', { month: '2-digit', day: '2-digit' });
				acc[date] = (acc[date] || 0) + item.price;
				return acc;
			}, {});

			salesData = Object.entries(salesByDate).slice(0, 7).reverse().map(([date, sales]) => ({
				x: date,
				y: sales
			}));

			totalSales = salesData.reduce((sum, data) => sum + data.y, 0);

			chartOptions.series = [{
				name: 'Sales',
				data: salesData,
				color: '#EF562F'
			}];

			chartOptions.xaxis.categories = salesData.map(data => data.x);
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	});

	let dark = false;

	function handler(ev: Event) {
		if ('detail' in ev) {
			chartOptions = chart_options_func(ev.detail);
			chartOptions.series = [{
				name: 'Sales',
				data: salesData,
				color: '#EF562F'
			}];
			dark = !!ev.detail;
		}
	}
</script>

<div class="space-y-4">
	<div class="grid gap-4 xl:grid-cols-2 2xl:grid-cols-3">
		<ChartWidget {chartOptions} title={`$${totalSales.toFixed(2)}`} subtitle="Sales this week" />

		<Stats />
	</div>
</div>
