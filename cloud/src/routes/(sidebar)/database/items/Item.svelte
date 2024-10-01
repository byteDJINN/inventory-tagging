<script lang="ts">
	import { Button, CloseButton, Heading, Input, Label, Search, Checkbox } from 'flowbite-svelte';
	import { CloseOutline } from 'flowbite-svelte-icons';
	import { createEventDispatcher, onMount } from 'svelte';
	import { pb } from '$lib/pocketbase';

	export let hidden: boolean = true;
	export let selectedItem: any = null;

	const dispatch = createEventDispatcher();

	let tagID: string = selectedItem?.tagID || '';
	let styleID: string = selectedItem?.styleID || '';
	let price: number = selectedItem?.price || 0;
	let sold: string | null = selectedItem?.sold || null;
	let isSold: boolean = selectedItem?.sold ? true : false;

	let styles: { id: string; name: string }[] = [];
	let filteredStyles: { id: string; name: string }[] = [];
	let styleSearchTerm: string = '';

	let showStyleDropdown = false;

	function toggleStyleDropdown() {
		showStyleDropdown = !showStyleDropdown;
	}

	function selectStyle(style: { id: string; name: string }) {
		styleID = style.id;
		styleSearchTerm = style.name;
		showStyleDropdown = false;
	}

	onMount(async () => {
		styles = await pb.collection('style').getFullList({ sort: 'name' });
		filteredStyles = styles;
		
		// Set the default style for the dropdown if editing an existing item
		if (selectedItem && selectedItem.styleID) {
			const selectedStyle = styles.find(style => style.id === selectedItem.styleID);
			if (selectedStyle) {
				styleSearchTerm = selectedStyle.name;
			}
		}
	});

	function calculateRelevance(style: any, searchTerms: string[]): number {
		let score = 0;
		const lowercaseName = style.name.toLowerCase();

		for (const term of searchTerms) {
			if (lowercaseName.includes(term)) {
				score += (term.length / lowercaseName.length);
			}
		}
		return score;
	}

	$: {
		if (styleSearchTerm) {
			const terms = styleSearchTerm.toLowerCase().split(' ');
			filteredStyles = styles
				.map(style => ({ ...style, score: calculateRelevance(style, terms) }))
				.sort((a, b) => b.score - a.score);
		} else {
			filteredStyles = styles;
		}
	}

	function handleSoldChange(event: Event) {
		const target = event.target as HTMLInputElement;
		if (target.checked) {
			sold = new Date().toISOString();
		} else {
			sold = null;
		}
	}

	async function handleSubmit() {
		try {
			const data = { tagID, styleID, price, sold };
			if (selectedItem) {
				await pb.collection('item').update(selectedItem.id, data);
			} else {
				await pb.collection('item').create(data);
			}
			dispatch('itemUpdated');
		} catch (error) {
			console.error('Error updating/creating item:', error);
		}
	}
</script>

<Heading tag="h5" class="mb-6 text-sm font-semibold uppercase">
	{selectedItem ? 'Update item' : 'Add new item'}
</Heading>
<CloseButton
	on:click={() => (hidden = true)}
	class="absolute right-2.5 top-2.5 text-gray-400 hover:text-black dark:text-white"
/>

<form on:submit|preventDefault={handleSubmit}>
	<div class="space-y-4">
		<Label class="space-y-2">
			<span>Tag ID</span>
			<Input
				name="tagID"
				class="border font-normal outline-none"
				placeholder="Enter tag ID"
				required
				bind:value={tagID}
			/>
		</Label>

		<Label class="space-y-2">
			<span>Style</span>
			<div class="relative">
				<Search class="font-normal"
                    size="md"
					bind:value={styleSearchTerm}
					placeholder="Search for a style"
					on:click={toggleStyleDropdown}
				/>
				{#if showStyleDropdown}
					<div class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
						{#each filteredStyles as style}
							<div
								class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
								on:click={() => selectStyle(style)}
							>
								{style.name}
							</div>
						{/each}
					</div>
				{/if}
			</div>
		</Label>

		<Label class="space-y-2">
			<span>Price</span>
			<Input
				name="price"
				type="number"
				step="0.01"
				class="border font-normal outline-none"
				placeholder="Enter price"
				required
				bind:value={price}
			/>
		</Label>

		<Label class="space-y-2 flex items-center">
			<Checkbox
				class="mr-2"
				checked={isSold}
				on:change={handleSoldChange}
			/>
			<span>Sold</span>
		</Label>

		<div class="bottom-0 left-0 flex w-full justify-center space-x-4 pb-4 md:absolute md:px-4">
			<Button type="submit" class="w-full">{selectedItem ? 'Update' : 'Add'}</Button>
			<Button color="alternative" class="w-full" on:click={() => (hidden = true)}>
				<CloseOutline />
				Cancel
			</Button>
		</div>
	</div>
</form>