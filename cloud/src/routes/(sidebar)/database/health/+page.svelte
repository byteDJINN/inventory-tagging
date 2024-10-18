<script lang="ts">
	import { Breadcrumb, BreadcrumbItem, Button, Heading, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Toolbar, Input, Spinner } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import { pb } from '$lib/pocketbase';
	import Footer from '../../Footer.svelte';

	let devices: {
		id: string,
		deviceName: string,
		alive: string | null
	}[] = [];
	let searchTerm: string = '';
	let isUpdating = false;

	onMount(async () => {
		await fetchDevices();
		// Set up an interval to fetch devices every 10 seconds
		setInterval(fetchDevices, 2000);
	});

	async function fetchDevices() {
		const fetchedDevices = await pb.collection("health").getFullList({
			sort: '-alive',
		});
		devices = fetchedDevices;
	}

	function getTimeDifference(timestamp: string | null): string {
		if (!timestamp) return 'Never';

		const now = new Date();
		const lastSeen = new Date(timestamp);
		const diffMs = now.getTime() - lastSeen.getTime();
		const diffMins = Math.floor(diffMs / 60000);
		const diffHours = Math.floor(diffMins / 60);
		const diffDays = Math.floor(diffHours / 24);

		if (diffMins < 1) return 'Just now';
		if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
		if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
		return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
	}

	function isOnline(timestamp: string | null): boolean {
		if (!timestamp) return false;
		const now = new Date();
		const lastSeen = new Date(timestamp);
		const diffMs = now.getTime() - lastSeen.getTime();
		const diffSeconds = Math.floor(diffMs / 1000);
		return diffSeconds <= 8;
	}

	$: filteredDevices = devices
		.sort((a, b) => {
			if (!a.alive) return 1;
			if (!b.alive) return -1;
			return new Date(b.alive).getTime() - new Date(a.alive).getTime();
		})
		.filter(device =>
			device.deviceName.toLowerCase().includes(searchTerm.toLowerCase())
		);
</script>

<main class="relative h-full w-full overflow-y-auto bg-white dark:bg-gray-800">
	<div class="p-4 flex justify-between items-center">
		<Heading tag="h1" class="text-xl font-semibold text-gray-900 dark:text-white sm:text-2xl">
			Device Health
		</Heading>
		{#if isUpdating}
			<span class="text-blue-500 animate-pulse">Updating...</span>
		{/if}
	</div>

	<div class="p-4">
		<Toolbar embedded class="w-full py-4 text-gray-500 dark:text-gray-400">
			<Input bind:value={searchTerm} placeholder="Search for devices" class="me-6 w-80 border xl:w-96" />
		</Toolbar> 
	</div>
	<div class="pl-4">
		<Table>
			<TableHead class="border-y border-gray-200 bg-gray-100 dark:border-gray-700">
				<TableHeadCell class="ps-4 font-normal w-1/3">Device Name</TableHeadCell>
				<TableHeadCell class="ps-4 font-normal w-1/3">Status</TableHeadCell>
				<TableHeadCell class="ps-4 font-normal w-1/3">Last Seen</TableHeadCell>
			</TableHead>
			<TableBody>
				{#each filteredDevices as device}
					<TableBodyRow class="text-base">
						<TableBodyCell class="p-4">{device.deviceName}</TableBodyCell>
						<TableBodyCell class="p-4">
							<span class={isOnline(device.alive) ? "text-green-500" : "text-red-500"}>
								{isOnline(device.alive) ? "Online" : "Offline"}
							</span>
						</TableBodyCell>
						<TableBodyCell class="p-4">{getTimeDifference(device.alive)}</TableBodyCell>
					</TableBodyRow>
				{/each}
			</TableBody>
		</Table>
	</div>
</main>
<Footer />
