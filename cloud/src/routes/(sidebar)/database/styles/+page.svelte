<script lang="ts">
	import { Breadcrumb, BreadcrumbItem, Button, Checkbox, Drawer, Heading, Input, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Toolbar, ToolbarButton } from 'flowbite-svelte';
	import { CogSolid, DotsVerticalOutline, EditOutline, ExclamationCircleSolid, TrashBinSolid, CirclePlusOutline } from 'flowbite-svelte-icons';
	import type { ComponentType } from 'svelte';
	import { sineIn } from 'svelte/easing';
	import Style from './Style.svelte';
	import { onMount } from 'svelte';
	import { pb } from '$lib/pocketbase';

	let hidden: boolean = true;
	let drawerComponent: ComponentType = Style;

	let styles: {
		collectionId: string,
		collectionName: string,
		created: string,
		id: string,
		name: string,
		description: string,
		updated: string
	}[] = [];
	let selectedStyle: any = null;
	let searchTerm: string = '';

	onMount(async () => {
		styles = await pb.collection("style").getFullList();
		styles.sort((a, b) => a.name.localeCompare(b.name));
	});

	function calculateRelevance(style: any, searchTerms: string[]): number {
		let score = 0;
		const lowercaseName = style.name.toLowerCase();
		const lowercaseDescription = style.description.toLowerCase();

		for (const term of searchTerms) {
			if (lowercaseName.includes(term)) {
				score += (term.length / lowercaseName.length);
			}
			if (lowercaseDescription.includes(term)) {
				score += (term.length / lowercaseDescription.length);
			}
		}
		return score;
	}

	$: sortedStyles = searchTerm
		? [...styles].sort((a, b) => {
				const terms = searchTerm.toLowerCase().split(' ');
				const scoreA = calculateRelevance(a, terms);
				const scoreB = calculateRelevance(b, terms);
				return scoreB - scoreA;
			})
		: styles;

	const toggle = (component: ComponentType, style: any = null) => {
		drawerComponent = component;
		selectedStyle = style;
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
			Styles
		</Heading>

		<Toolbar embedded class="w-full py-4 text-gray-500 dark:text-gray-400">
			<Input bind:value={searchTerm} placeholder="Search for styles" class="me-6 w-80 border xl:w-96" />

			<div slot="end" class="space-x-2">
				<Button size="sm" class="gap-2" on:click={() => toggle(Style)}>
					<CirclePlusOutline size="sm" /> Add
				</Button>
			</div>
		</Toolbar> 
	</div>
	<div class="pl-4">
	<Table>
		<TableHead class="border-y border-gray-200 bg-gray-100 dark:border-gray-700">
			{#each ['Name', 'Description', 'Actions'] as title}
				<TableHeadCell class="ps-4 font-normal">{title}</TableHeadCell>
			{/each}
		</TableHead>
		<TableBody>
			{#each sortedStyles as style}
				<TableBodyRow class="text-base">
					<TableBodyCell class="p-4">{style.name}</TableBodyCell>
					<TableBodyCell class="max-w-sm overflow-hidden truncate p-4 text-gray-500 dark:text-gray-400 xl:max-w-xs">{style.description}</TableBodyCell>
					<TableBodyCell class="space-x-2">
						<Button size="xs" class="gap-2 px-3" on:click={() => toggle(Style, style)}>
							<EditOutline size="sm" /> Update
						</Button>
					</TableBodyCell>
				</TableBodyRow>
			{/each}
		</TableBody>
	</Table>
	</div>
</main>

<Drawer placement="right" transitionType="fly" {transitionParams} bind:hidden>
	<svelte:component 
		this={drawerComponent} 
		bind:hidden 
		selectedStyle={selectedStyle} 
		on:styleUpdated={async () => {
			hidden = true;
			styles = await pb.collection("style").getFullList();
		}} 
	/>
</Drawer>