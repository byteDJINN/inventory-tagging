<script lang="ts">
	import { Breadcrumb, BreadcrumbItem, Button, Checkbox, Drawer, Heading, Input, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Toolbar, ToolbarButton, Spinner } from 'flowbite-svelte';
	import { CogSolid, DotsVerticalOutline, EditOutline, ExclamationCircleSolid, TrashBinSolid, FileCopySolid, CirclePlusOutline, ChevronDownOutline, ChevronUpOutline } from 'flowbite-svelte-icons';
	import type { ComponentType } from 'svelte';
	import { sineIn } from 'svelte/easing';
	import Item from './Item.svelte';
	import { onMount } from 'svelte';
	import { pb } from '$lib/pocketbase';

	let hidden: boolean = true;
	let drawerComponent: ComponentType = Item;
	let selectedItem: any = null;

	let items: {
		id: string,
		name: string,
		size: string,
		colour: string,
		price: number,
		timeSold: string | null
	}[] = [];
	let searchTerm: string = '';

	let styles: {
		name: string,
		items: typeof items
	}[] = [];
	let expandedStyles: Set<string> = new Set();

    let updateQueue: (() => Promise<void>)[] = [];
    let isUpdating = false;

    $: console.log(updateQueue);

	onMount(async () => {
		const fetchedItems = await pb.collection("items").getFullList();

		// Group items by name (which now represents the style)
		const groupedItems = fetchedItems.reduce((acc, item) => {
			if (!acc[item.name]) {
				acc[item.name] = [];
			}
			acc[item.name].push(item);
			return acc;
		}, {});

		styles = Object.entries(groupedItems).map(([name, items]) => ({
			name,
			items: items as typeof fetchedItems
		}));

		styles.sort((a, b) => a.name.localeCompare(b.name));
	});

	function calculateRelevance(item: any, searchTerms: string[]): number {
		let score = 0;
		const lowercaseName = item.name.toLowerCase();
		const lowercaseSize = item.size.toLowerCase();
		const lowercaseColour = item.colour.toLowerCase();
		const price = item.price.toString();
		const soldDate = item.timeSold ? new Date(item.timeSold).toLocaleDateString('en-AU').toLowerCase() : '';

		for (const term of searchTerms) {
			if (lowercaseName.includes(term)) score += (term.length / lowercaseName.length);
			if (lowercaseSize.includes(term)) score += (term.length / lowercaseSize.length);
			if (lowercaseColour.includes(term)) score += (term.length / lowercaseColour.length);
			if (price.includes(term)) score += (term.length / price.length);
			if (soldDate.includes(term)) score += (term.length / soldDate.length);
		}
		return score;
	}

	$: sortedStyles = searchTerm
		? [...styles].sort((a, b) => {
				const terms = searchTerm.toLowerCase().split(' ');
				const maxScoreA = Math.max(...a.items.map(item => calculateRelevance(item, terms)));
				const maxScoreB = Math.max(...b.items.map(item => calculateRelevance(item, terms)));
				return maxScoreB - maxScoreA;
			})
		: styles;

	$: sortedItems = (style: any) => {
		if (!searchTerm) {
			return [...style.items].sort((a, b) => {
				// Sort unsold items first
				if (!a.timeSold && b.timeSold) return -1;
				if (a.timeSold && !b.timeSold) return 1;
				// If both are sold, sort by sold time (most recent first)
				if (a.timeSold && b.timeSold) {
					return new Date(b.timeSold).getTime() - new Date(a.timeSold).getTime();
				}
				return 0;
			});
		}
		const terms = searchTerm.toLowerCase().split(' ');
		return [...style.items].sort((a, b) => {
			const scoreA = calculateRelevance(a, terms);
			const scoreB = calculateRelevance(b, terms);
			if (scoreA !== scoreB) return scoreB - scoreA;
			// If relevance scores are equal, apply the same sorting as above
			if (!a.timeSold && b.timeSold) return -1;
			if (a.timeSold && !b.timeSold) return 1;
			if (a.timeSold && b.timeSold) {
				return new Date(b.timeSold).getTime() - new Date(a.timeSold).getTime();
			}
			return 0;
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

	function toggleStyle(styleName: string) {
		if (expandedStyles.has(styleName)) {
			expandedStyles.delete(styleName);
		} else {
			expandedStyles.add(styleName);
		}
		expandedStyles = expandedStyles;
	}

    // Debounce function
    function debounce(func: Function, delay: number) {
        let timeoutId: NodeJS.Timeout;
        return (...args: any[]) => {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func(...args), delay);
        };
    }

    // Queue update function
    const queueUpdate = (update: () => Promise<void>) => {
        updateQueue = [...updateQueue, update];
        processQueue();
    };

    // Process queue function
    async function processQueue() {
        if (isUpdating || updateQueue.length === 0) return;
        isUpdating = true;
        while (updateQueue.length > 0) {
            const update = updateQueue[0];
            if (update) await update();
            updateQueue = updateQueue.slice(1);
        }
        isUpdating = false;
    }

	function updateStyles(updatedItem: any) {
		styles = styles.map(style => {
			// Remove the item from its current style if it exists
			style.items = style.items.filter(item => item.id !== updatedItem.id);
			
			// Add the item to its new style
			if (style.name === updatedItem.name) {
				style.items.push(updatedItem);
			}
			
			return style;
		});

		// If the updated item's style doesn't exist, create a new style
		if (!styles.some(style => style.name === updatedItem.name)) {
			styles = [...styles, { name: updatedItem.name, items: [updatedItem] }];
		}
		
		// if any styles are empty delete them
		styles = styles.filter(style => style.items.length > 0);

		// Sort styles alphabetically
		styles.sort((a, b) => a.name.localeCompare(b.name));

		// Ensure the view updates
		styles = styles;
	}

	function duplicateItem(item: any) {
		const duplicatedItem = { ...item, id: null };
		toggle(Item, duplicatedItem);
	}

</script>

<main class="relative h-full w-full overflow-y-auto bg-white dark:bg-gray-800">
	<div class="p-4">
		<Heading tag="h1" class="text-xl font-semibold text-gray-900 dark:text-white sm:text-2xl">
			Items
		</Heading>

		<Toolbar embedded class="w-full py-4 text-gray-500 dark:text-gray-400">
			<Input bind:value={searchTerm} placeholder="Search for items" class="me-6 w-80 border xl:w-96" />

			<div slot="end" class="space-x-4 flex items-center">
                {#if updateQueue.length > 0}
                    <Spinner size="6" color="gray" />
                {/if}
                <Button size="xs" class="gap-2" on:click={() => toggle(Item)}>
                    <CirclePlusOutline size="sm" /> New Item
                </Button>
            </div>
		</Toolbar> 
	</div>
    <div class="pl-4">
	<Table>
		<TableHead class="border-y border-gray-200 bg-gray-100 dark:border-gray-700">
			<TableHeadCell class="ps-4 font-normal w-1/4">Style</TableHeadCell>
			<TableHeadCell class="ps-4 font-normal w-1/4">Stock</TableHeadCell>
			<TableHeadCell class="ps-4 font-normal w-1/4">Sold</TableHeadCell>
			<TableHeadCell class="ps-4 font-normal w-1/4">Actions</TableHeadCell>
		</TableHead>
		<TableBody>
			{#each sortedStyles as style}
				<TableBodyRow class="text-base">
					<TableBodyCell class="p-4">{style.name}</TableBodyCell>
					<TableBodyCell class="p-4">{style.items.filter(item => !item.timeSold).length}</TableBodyCell>
					<TableBodyCell class="p-4">{style.items.filter(item => item.timeSold).length}</TableBodyCell>
					<TableBodyCell class="space-x-2">
						<Button size="xs" class="gap-2 px-3" on:click={() => toggleStyle(style.name)}>
							{#if expandedStyles.has(style.name)}
								<ChevronUpOutline size="sm" /> Hide Items
							{:else}
								<ChevronDownOutline size="sm" /> Show Items
							{/if}
						</Button>
					</TableBodyCell>
				</TableBodyRow>
				{#if expandedStyles.has(style.name)}
					<TableBodyRow>
						<TableBodyCell colspan="4" class="p-0 pl-[4%]">
							<Table>
								<TableHead class="bg-gray-100 dark:border-gray-700">
									<TableHeadCell class="ps-8 font-normal w-1/6">Size</TableHeadCell>
									<TableHeadCell class="ps-8 font-normal w-1/6">Colour</TableHeadCell>
									<TableHeadCell class="ps-8 font-normal w-1/6">Price</TableHeadCell>
									<TableHeadCell class="ps-8 font-normal w-1/6">Sold</TableHeadCell>
									<TableHeadCell class="ps-8 font-normal w-2/6">Actions</TableHeadCell>
								</TableHead>
								<TableBody>
									{#each sortedItems(style) as item}
										<TableBodyRow>
											<TableBodyCell class="ps-8">{item.size}</TableBodyCell>
											<TableBodyCell class="ps-8">{item.colour}</TableBodyCell>
											<TableBodyCell>${item.price}</TableBodyCell>
											<TableBodyCell>
												{#if item.timeSold}
													{new Date(item.timeSold).toLocaleDateString('en-AU')}
												{:else}
													Not sold
												{/if}
											</TableBodyCell>
											<TableBodyCell>
												<Button size="xs" class="gap-2" on:click={() => toggle(Item, item)}>
													<EditOutline size="sm" /> Edit
												</Button>
												<Button size="xs" class="gap-2 ml-2" on:click={() => duplicateItem(item)}>
													<FileCopySolid size="sm" /> Duplicate
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
		{queueUpdate}
        {updateStyles}
	/>
</Drawer>