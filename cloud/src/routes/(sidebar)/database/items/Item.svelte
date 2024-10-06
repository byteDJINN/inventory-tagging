<script lang="ts">
	import { Button, CloseButton, Heading, Input, Label, Checkbox } from 'flowbite-svelte';
	import { CloseOutline } from 'flowbite-svelte-icons';
	import { pb } from '$lib/pocketbase';

	export let hidden: boolean = true;
	export let selectedItem: any = null;
	export let queueUpdate: (update: () => Promise<void>, immediateUpdate: () => void) => void;
	export let updateStyles: (item: any, isNew: boolean) => void;

	let tagID: string = selectedItem?.tagID || '';
	let name: string = selectedItem?.name || '';
	let size: string = selectedItem?.size || '';
	let colour: string = selectedItem?.colour || '';
	let price: number = selectedItem?.price || 0;
	let timeSold: string | null = selectedItem?.timeSold || null;
	let isSold: boolean = selectedItem?.timeSold ? true : false;

	function handleSoldChange(event: Event) {
		const target = event.target as HTMLInputElement;
		if (target.checked) {
			timeSold = new Date().toISOString();
		} else {
			timeSold = null;
		}
	}

	function handleSubmit() {
		const newItem = { id: selectedItem?.id, tagID, name, size, colour, price, timeSold };
		const isNew = !selectedItem;

		const updateFunction = async () => {
			try {
				if (selectedItem) {
					await pb.collection('items').update(selectedItem.id, newItem);
				} else {
					const createdItem = await pb.collection('items').create(newItem);
					newItem.id = createdItem.id;
				}
			} catch (error) {
				console.error('Error updating/creating item:', error);
				// Here you might want to revert the UI change if the database update fails
			}
		};

		const immediateUpdate = () => {
			updateStyles(newItem, isNew);
			hidden = true;
		};

		queueUpdate(updateFunction, immediateUpdate);
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
			<span>Name (Style)</span>
			<Input
				name="name"
				class="border font-normal outline-none"
				placeholder="Enter name/style"
				required
				bind:value={name}
			/>
		</Label>

		<Label class="space-y-2">
			<span>Size</span>
			<Input
				name="size"
				class="border font-normal outline-none"
				placeholder="Enter size"
				required
				bind:value={size}
			/>
		</Label>

		<Label class="space-y-2">
			<span>Colour</span>
			<Input
				name="colour"
				class="border font-normal outline-none"
				placeholder="Enter colour"
				required
				bind:value={colour}
			/>
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