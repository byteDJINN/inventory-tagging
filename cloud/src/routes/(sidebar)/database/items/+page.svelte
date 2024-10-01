<script lang="ts">
	import { Breadcrumb, BreadcrumbItem, Button, Checkbox, Drawer, Heading, Input, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Toolbar, ToolbarButton, MultiSelect, Spinner } from 'flowbite-svelte';
	import { CogSolid, DotsVerticalOutline, EditOutline, ExclamationCircleSolid, TrashBinSolid, CirclePlusOutline, ChevronDownOutline, ChevronUpOutline, PlusOutline, MinusOutline, TagSolid } from 'flowbite-svelte-icons';
	import type { ComponentType } from 'svelte';
	import { sineIn } from 'svelte/easing';
	import Item from './Item.svelte';
	import { onMount } from 'svelte';
	import { pb } from '$lib/pocketbase';
	import AttributeSelector from './AttributeSelector.svelte';

	let hidden: boolean = true;
	let drawerComponent: ComponentType = Item;
	let drawerItem: any = null;

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
			sold: string | null,
			attributes: string[]
		}[]
	}[] = [];
	let expandedStyles: Set<string> = new Set();

	let availableAttributes: string[] = [];

    let updateQueue: (() => Promise<void>)[] = [];
    let isUpdating = false;

    $: console.log(updateQueue);

	onMount(async () => {
		const fetchedItems = await pb.collection("item").getFullList();
		const fetchedStyles = await pb.collection("style").getFullList();
		const fetchedItemAttributes = await pb.collection("itemattribute").getFullList({
			expand: 'attributeID'
		});
		const fetchedAttributes = await pb.collection("attribute").getFullList();

		availableAttributes = fetchedAttributes.map(attr => `${attr.type}: ${attr.value}`);

		styles = fetchedStyles.map(style => ({
			...style,
			items: fetchedItems.filter(item => item.styleID === style.id).map(item => ({
				...item,
				attributes: fetchedItemAttributes
					.filter(ia => ia.itemID === item.id)
					.map(ia => `${ia.expand.attributeID.type}: ${ia.expand.attributeID.value}`)
			}))
		}));

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

	async function updateItemAttributes(itemId: string, selection: {name: string, value: string}[]) {
		let newAttributes: string[] = selection.map(item => item.value);
		
		// Fetch current attributes for the item from the database
		const currentItemAttributes = await pb.collection("itemattribute").getFullList({
			filter: `itemID="${itemId}"`,
			expand: 'attributeID'
		});

		const currentAttributes = currentItemAttributes.map(ia => 
			`${ia.expand.attributeID.type}: ${ia.expand.attributeID.value}`
		);

        // if they are the same dont continue
        if (currentAttributes.length === newAttributes.length && currentAttributes.every(attr => newAttributes.includes(attr))) {
            return;
        }
		

		// Attributes to add
		const attributesToAdd = newAttributes.filter(attr => !currentAttributes.includes(attr));

		// Attributes to remove
		const attributesToRemove = currentItemAttributes.filter(ia => 
			!newAttributes.includes(`${ia.expand.attributeID.type}: ${ia.expand.attributeID.value}`)
		);

		// Remove attributes
		for (const ia of attributesToRemove) {
			await pb.collection("itemattribute").delete(ia.id);
		}

		// Add new attributes
		for (const attr of attributesToAdd) {
			const [type, value] = attr.split(': ');
			const attribute = await pb.collection("attribute").getFirstListItem(`type="${type}" && value="${value}"`);
			await pb.collection("itemattribute").create({
				itemID: itemId,
				attributeID: attribute.id
			});
		}

		// After updating, refresh the item's attributes
		const updatedItemAttributes = await pb.collection("itemattribute").getFullList({
			filter: `itemID="${itemId}"`,
			expand: 'attributeID'
		});


		// Update the item in the styles array
		styles = styles.map(style => ({
			...style,
			items: style.items.map(item => 
				item.id === itemId 
					? {
							...item,
							attributes: updatedItemAttributes.map(ia => 
								`${ia.expand.attributeID.type}: ${ia.expand.attributeID.value}`
							)
						}
					: item
			)
		}));
	}

	function openAttributeSelector(item: any) {
		drawerComponent = AttributeSelector;
		drawerItem = item;
		hidden = false;
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
    const queueUpdate = debounce((selectedAttributes: string[]) => {
        if (drawerItem == null) {
            return ;
        }
        updateQueue = [...updateQueue, async () => {
            await updateItemAttributes(drawerItem.id, selectedAttributes.map(attr => ({ name: attr, value: attr })));
        }];
        processQueue();
    }, 300);

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
			<TableHeadCell class="ps-4 font-normal w-8"></TableHeadCell>
			<TableHeadCell class="ps-4 font-normal w-1/4">Style</TableHeadCell>
			<TableHeadCell class="ps-4 font-normal w-1/2">Description</TableHeadCell>
			<TableHeadCell class="ps-4 font-normal w-1/4">Actions</TableHeadCell>
		</TableHead>
		<TableBody>
			{#each sortedStyles as style}
				<TableBodyRow class="text-base">
					<TableBodyCell class="p-4"></TableBodyCell>
					<TableBodyCell class="p-4">{style.name}</TableBodyCell>
					<TableBodyCell class="max-w-sm text-sm overflow-hidden truncate p-4 text-gray-500 dark:text-gray-400 xl:max-w-xs">
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
						<TableBodyCell colspan="4" class="p-0 pl-[4%]">
							<Table>
								<TableHead class="bg-gray-100 dark:border-gray-700">
									<TableHeadCell class="ps-8 font-normal w-1/5">Tag ID</TableHeadCell>
									<TableHeadCell class="ps-8 font-normal w-1/5">Price</TableHeadCell>
									<TableHeadCell class="ps-8 font-normal w-1/5">Sold</TableHeadCell>
									<TableHeadCell class="ps-8 font-normal w-2/5">Attributes</TableHeadCell>
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
											<TableBodyCell class="max-w-xs">
												<div class="flex items-center">
													<div class="max-h-16 rounded p-1 w-full overflow-y-auto overflow-x-hidden text-sm hover:bg-gray-100 hover:cursor-pointer"
                                                     on:click={() => openAttributeSelector(item)}>
														{#if item.attributes.length > 0}
															<ul>
																{#each item.attributes.sort((a, b) => a.localeCompare(b)) as attribute}
																	<li>{attribute}</li>
																{/each}
															</ul>
														{:else}
															<span class="text-gray-500">No attributes</span>
														{/if}
													</div>
												</div>
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
        {drawerItem}
        {updateItemAttributes}
		{availableAttributes}
        {updateQueue}
        {queueUpdate}
	/>
</Drawer>