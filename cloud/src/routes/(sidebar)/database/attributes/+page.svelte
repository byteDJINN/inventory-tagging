<script lang="ts">
	import { Breadcrumb, BreadcrumbItem, Button, Checkbox, Drawer, Heading, Input, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Toolbar, ToolbarButton } from 'flowbite-svelte';
	import { CogSolid, DotsVerticalOutline, EditOutline, ExclamationCircleSolid, TrashBinSolid, CirclePlusOutline } from 'flowbite-svelte-icons';
	import type { ComponentType } from 'svelte';
	import { sineIn } from 'svelte/easing';
	import Attribute from './Attribute.svelte';
	import { onMount } from 'svelte';
	import { pb } from '$lib/pocketbase';

	let hidden: boolean = true; // modal control
	let drawerComponent: ComponentType = Attribute; // drawer component

	let attributes: {
		collectionId: string,
		collectionName: string,
		created: string,
		id: string,
		type: string,
		updated: string,
		value: string
	}[] = [];
	let selectedAttribute: any = null;

	onMount(async () => {
		attributes = await pb.collection("attribute").getFullList();
	});

	const toggle = (component: ComponentType, attribute: any = null) => {
		drawerComponent = component;
		selectedAttribute = attribute;
		hidden = !hidden;
	};

	let transitionParams = {
		x: 320,
		duration: 200,
		easing: sineIn
	};
</script>


<main class="relative h-full w-full overflow-y-auto bg-white dark:bg-gray-800">
	<div class="p-4">
		<Heading tag="h1" class="text-xl font-semibold text-gray-900 dark:text-white sm:text-2xl">
			Attributes
		</Heading>

		<Toolbar embedded class="w-full py-4 text-gray-500 dark:text-gray-400">
			<Input placeholder="Search for products" class="me-6 w-80 border xl:w-96" />
			<ToolbarButton
				color="dark"
				class="m-0 rounded p-1 hover:bg-gray-100 focus:ring-0 dark:hover:bg-gray-700"
			>
				<CogSolid size="lg" />
			</ToolbarButton>
			<ToolbarButton
				color="dark"
				class="m-0 rounded p-1 hover:bg-gray-100 focus:ring-0 dark:hover:bg-gray-700"
			>
				<TrashBinSolid size="lg" />
			</ToolbarButton>
			<ToolbarButton
				color="dark"
				class="m-0 rounded p-1 hover:bg-gray-100 focus:ring-0 dark:hover:bg-gray-700"
			>
				<ExclamationCircleSolid size="lg" />
			</ToolbarButton>
			<ToolbarButton
				color="dark"
				class="m-0 rounded p-1 hover:bg-gray-100 focus:ring-0 dark:hover:bg-gray-700"
			>
				<DotsVerticalOutline size="lg" />
			</ToolbarButton>

			<div slot="end" class="space-x-2">
				<Button size="sm" class="gap-2" on:click={() => toggle(Attribute)}>
					<CirclePlusOutline size="sm" /> Add
				</Button>
			</div>
		</Toolbar> 
	</div>
	<Table>
		<TableHead class="border-y border-gray-200 bg-gray-100 dark:border-gray-700">
			<TableHeadCell class="w-4 p-4"><Checkbox /></TableHeadCell>
			{#each ['Type', 'Value', 'Actions'] as title}
				<TableHeadCell class="ps-4 font-normal">{title}</TableHeadCell>
			{/each}
		</TableHead>
		<TableBody>
			{#each attributes as attribute}
				<TableBodyRow class="text-base">
					<TableBodyCell class="w-4 p-4"><Checkbox /></TableBodyCell>
					<TableBodyCell class="p-4">{attribute.type}</TableBodyCell>
					<TableBodyCell class="p-4">{attribute.value}</TableBodyCell>
					<TableBodyCell class="space-x-2">
						<Button size="xs" class="gap-2 px-3" on:click={() => toggle(Attribute, attribute)}>
							<EditOutline size="sm" /> Update
						</Button>
					</TableBodyCell>
				</TableBodyRow>
			{/each}
		</TableBody>
	</Table>
</main>


<Drawer placement="right" transitionType="fly" {transitionParams} bind:hidden>
	<svelte:component 
		this={drawerComponent} 
		bind:hidden 
		selectedAttribute={selectedAttribute} 
		on:attributeUpdated={async () => {
			hidden = true;
			attributes = await pb.collection("attribute").getFullList();
		}} 
	/>
</Drawer>
