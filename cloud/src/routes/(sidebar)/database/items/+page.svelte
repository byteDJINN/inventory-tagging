<script lang="ts">
	import { Breadcrumb, BreadcrumbItem, Button, Checkbox, Drawer, Heading, Input, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Toolbar, ToolbarButton } from 'flowbite-svelte';
	import { CogSolid, DotsVerticalOutline, EditOutline, ExclamationCircleSolid, TrashBinSolid, CirclePlusOutline, ChevronDownOutline, ChevronUpOutline } from 'flowbite-svelte-icons';
	import type { ComponentType } from 'svelte';
	import { sineIn } from 'svelte/easing';
	import Item from './Item.svelte';
	import { onMount } from 'svelte';
	import { pb } from '$lib/pocketbase';

	let hidden: boolean = true;
	let drawerComponent: ComponentType = Item;

	let items: {
		id: string,
		tagID: string,
		styleID: string,
		price: number,
		sold: string | null,
		style?: { name: string }
	}[] = [];
	let selectedItem: any = null;
	let searchTerm: string = '';

	let styles: {
		id: string,
		name: string,
		description: string,
		items: {
			id: string,
			tagID: string,
			price: number,
			sold: string | null
		}[]
	}[] = [];
	let expandedStyles: Set<string> = new Set();

	onMount(async () => {
		const fetchedItems = await pb.collection("item").getFullList();
		const fetchedStyles = await pb.collection("style").getFullList();

		styles = fetchedStyles.map(style => ({
			...style,
			items: fetchedItems.filter(item => item.styleID === style.id)
		}));

		// Remove average sold price calculation

		styles.sort((a, b) => a.name.localeCompare(b.name));
	});

	function calculateRelevance(item: any, searchTerms: string[]): number {
		let score = 0;
		const lowercaseTagID = item.tagID.toLowerCase();
		const lowercaseStyleName = item.style?.name.toLowerCase() || '';
		const lowercaseStyleDescription = item.style?.description.toLowerCase() || '';
		const price = item.price.toString();
		const soldDate = item.sold ? new Date(item.sold).toLocaleDateString('en-AU').toLowerCase() : '';

		for (const term of searchTerms) {
			if (lowercaseTagID.includes(term)) {
				score += (term.length / lowercaseTagID.length);
			}
			if (lowercaseStyleName.includes(term)) {
				score += (term.length / lowercaseStyleName.length);
			}
			if (lowercaseStyleDescription.includes(term)) {
				score += (term.length / lowercaseStyleDescription.length) * 0.5; // Lower weight for description
			}
			if (price.includes(term)) {
				score += (term.length / price.length); // Relative match for price
			}
			if (soldDate.includes(term)) {
				score += (term.length / soldDate.length); // Relative match for sold date
			}
		}
		return score;
	}

	$: sortedStyles = searchTerm
		? [...styles].sort((a, b) => {
				const terms = searchTerm.toLowerCase().split(' ');
				const maxScoreA = Math.max(...a.items.map(item => calculateRelevance({...item, style: a}, terms)));
				const maxScoreB = Math.max(...b.items.map(item => calculateRelevance({...item, style: b}, terms)));
				return maxScoreB - maxScoreA;
			})
		: styles;

	$: sortedItems = (style: any) => {
		if (!searchTerm) return style.items;
		const terms = searchTerm.toLowerCase().split(' ');
		return [...style.items].sort((a, b) => {
			const scoreA = calculateRelevance({...a, style}, terms);
			const scoreB = calculateRelevance({...b, style}, terms);
			return scoreB - scoreA;
		});
	};

	const toggle = (component: ComponentType, item: any = null) => {
		drawerComponent = component;
		selectedItem = item;
		hidden = !hidden;
	};

	let transitionParams = {
		x: 320,
		duration: 200,
		easing: sineIn
	};

	function toggleStyle(styleId: string) {
		if (expandedStyles.has(styleId)) {
			expandedStyles.delete(styleId);
		} else {
			expandedStyles.add(styleId);
		}
		expandedStyles = expandedStyles;
	}
</script>

<main class="relative h-full w-full overflow-y-auto bg-white dark:bg-gray-800">
	<div class="p-4">
		<Heading tag="h1" class="text-xl font-semibold text-gray-900 dark:text-white sm:text-2xl">
			Items
		</Heading>

		<Toolbar embedded class="w-full py-4 text-gray-500 dark:text-gray-400">
			<Input bind:value={searchTerm} placeholder="Search for items" class="me-6 w-80 border xl:w-96" />

			<div slot="end" class="space-x-2">
				<Button size="sm" class="gap-2" on:click={() => toggle(Item)}>
					<CirclePlusOutline size="sm" /> Add
				</Button>
			</div>
		</Toolbar> 
	</div>
    <div class="pl-4">
	<Table>
		<TableHead class="border-y border-gray-200 bg-gray-100 dark:border-gray-700">
			{#each ['Style', 'Description', 'Actions'] as title}
				<TableHeadCell class="ps-4 font-normal">{title}</TableHeadCell>
			{/each}
		</TableHead>
		<TableBody>
			{#each sortedStyles as style}
				<TableBodyRow class="text-base">
					<TableBodyCell class="p-4">{style.name}</TableBodyCell>
					<TableBodyCell class="max-w-sm overflow-hidden truncate p-4 text-gray-500 dark:text-gray-400 xl:max-w-xs">
                        {style.description}
					</TableBodyCell>
					<TableBodyCell class="space-x-2">
						<Button size="xs" class="gap-2 px-3" on:click={() => toggleStyle(style.id)}>
							{#if expandedStyles.has(style.id)}
								<ChevronUpOutline size="sm" /> Hide Items
							{:else}
								<ChevronDownOutline size="sm" /> Show Items
							{/if}
						</Button>
					</TableBodyCell>
				</TableBodyRow>
				{#if expandedStyles.has(style.id)}
					<TableBodyRow>
						<TableBodyCell colspan="5" class="p-0 pl-[4%]">
							<Table>
								<TableHead class=" bg-gray-100 dark:border-gray-700">
									{#each ["Tag ID", "Price", "Sold", "Actions"] as title}
										<TableHeadCell class="ps-8 font-normal">{title}</TableHeadCell>
									{/each}
								</TableHead>
								<TableBody>
									{#each sortedItems(style) as item}
										<TableBodyRow>
											<TableBodyCell class="ps-8">{item.tagID}</TableBodyCell>
											<TableBodyCell>${item.price.toFixed(2)}</TableBodyCell>
											<TableBodyCell>
												{#if item.sold}
													{new Date(item.sold).toLocaleDateString('en-AU')}
												{:else}
													Not sold
												{/if}
											</TableBodyCell>
											<TableBodyCell>
												<Button size="xs" class="gap-2 px-3" on:click={() => toggle(Item, item)}>
													<EditOutline size="sm" /> Update
												</Button>
											</TableBodyCell>
										</TableBodyRow>
									{/each}
								</TableBody>
							</Table>
						</TableBodyCell>
					</TableBodyRow>
				{/if}
			{/each}
		</TableBody>
	</Table>
    </div>
</main>

<Drawer placement="right" transitionType="fly" {transitionParams} bind:hidden>
	<svelte:component 
		this={drawerComponent} 
		bind:hidden 
		selectedItem={selectedItem} 
		on:itemUpdated={async () => {
			hidden = true;
			items = await pb.collection("item").getFullList({
				expand: 'style'
			});
		}} 
	/>
</Drawer>