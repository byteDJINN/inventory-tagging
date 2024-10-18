<script lang="ts">
	import { Card, Heading, Popover, TabItem, Tabs } from 'flowbite-svelte';
	import Change from '../../utils/dashboard/Change.svelte';
	import { imagesPath } from '../../utils/variables';
	import LastRange from '../widgets/LastRange.svelte';
	import More from '../widgets/More.svelte';
	import { QuestionCircleSolid } from 'flowbite-svelte-icons';
	import { onMount } from 'svelte';
	import { pb } from '$lib/pocketbase';

	let topProducts: {
		name: string,
		totalSales: number,
		change: number,
		image: string
	}[] = [];

	let requestQueue: (() => Promise<void>)[] = [];
	let isProcessing = false;

	async function processQueue() {
		if (isProcessing) return;
		isProcessing = true;

		while (requestQueue.length > 0) {
			const request = requestQueue.shift();
			if (request) {
				await request();
			}
		}

		isProcessing = false;
	}

	function queueRequest(request: () => Promise<void>) {
		requestQueue.push(request);
		processQueue();
	}

	onMount(() => {
		queueRequest(async () => {
			try {
				const currentDate = new Date();
				const lastMonthDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, currentDate.getDate());

				const currentMonthRecords = await pb.collection('items').getFullList({
					sort: '-timeSold',
					filter: `timeSold >= "${currentDate.toISOString().split('T')[0]}" && timeSold != null`,
					requestKey: 'current_' + Date.now().toString()
				});

				const lastMonthRecords = await pb.collection('items').getFullList({
					sort: '-timeSold',
					filter: `timeSold >= "${lastMonthDate.toISOString().split('T')[0]}" && timeSold < "${currentDate.toISOString().split('T')[0]}"`,
					requestKey: 'last_' + Date.now().toString()
				});

				const currentMonthSales = calculateSales(currentMonthRecords);
				const lastMonthSales = calculateSales(lastMonthRecords);

				topProducts = Object.entries(currentMonthSales)
					.map(([name, data]) => {
						const lastMonthTotal = lastMonthSales[name]?.totalSales || 0;
						const change = lastMonthTotal > 0
							? ((data.totalSales - lastMonthTotal) / lastMonthTotal) * 100
							: 100; // If there were no sales last month, consider it a 100% increase

						return {
							name,
							totalSales: data.totalSales,
							change: Number(change.toFixed(2)),
							image: data.image
						};
					})
					.sort((a, b) => b.totalSales - a.totalSales)
					.slice(0, 5);
			} catch (error) {
				console.error('Error fetching top products:', error);
			}
		});
	});

	function calculateSales(records) {
		return records.reduce((acc, item) => {
			if (!acc[item.name]) {
				acc[item.name] = { totalSales: 0, count: 0, image: item.image };
			}
			acc[item.name].totalSales += item.price;
			acc[item.name].count += 1;
			return acc;
		}, {});
	}
</script>

<Card size="xl">
	<div class="mb-4 flex items-center gap-2">
		<Heading tag="h3" class="w-fit text-lg font-semibold dark:text-white">
			Statistics this month
		</Heading>
	</div>
	<Tabs
		style="full"
		defaultClass="flex divide-x rtl:divide-x-reverse divide-gray-200 shadow dark:divide-gray-700"
		contentClass="p-3 mt-4"
	>
		<TabItem class="w-full" open>
			<span slot="title">Top products</span>
			<ul class="-m-3 divide-y divide-gray-200 dark:divide-gray-700 dark:bg-gray-800">
				{#each topProducts as { name, totalSales, change, image }}
					<li class="py-3 sm:py-4">
						<div class="flex items-center justify-between">
							<div class="flex min-w-0 items-center">
								<div class="ml-3">
									<p class="truncate font-medium text-gray-900 dark:text-white">
										{name}
									</p>
									<Change value={change} size="sm" equalHeight class="ml-px" />
								</div>
							</div>
							<div
								class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
							>
								${totalSales}
							</div>
						</div>
					</li>
				{/each}
			</ul>
		</TabItem>
	</Tabs>

</Card>
