<script lang="ts">
	import { Button, CloseButton, Heading, Input, Label } from 'flowbite-svelte';
	import { CloseOutline } from 'flowbite-svelte-icons';
	import { pb } from '$lib/pocketbase';

	export let hidden: boolean = true;
	export let selectedItem: any = null;
	export let queueUpdate: (update: () => Promise<void>) => void;
	export let updateStyles: (upatedItem: any) => void;

	let name: string = selectedItem?.name || '';
	let size: string = selectedItem?.size || '';
	let colour: string = selectedItem?.colour || '';
	let price: number = selectedItem?.price || 0;
	let timeSold: string | null = selectedItem?.timeSold ? formatDateTimeLocal(selectedItem.timeSold) : null;

	function formatDateTimeLocal(isoString: string): string {
		const date = new Date(isoString);
		const year = date.getFullYear();
		const month = String(date.getMonth() + 1).padStart(2, '0');
		const day = String(date.getDate()).padStart(2, '0');
		const hours = String(date.getHours()).padStart(2, '0');
		const minutes = String(date.getMinutes()).padStart(2, '0');
		return `${year}-${month}-${day}T${hours}:${minutes}`;
	}

	async function generateUniqueId(): Promise<string> {
		const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
		let id: string;
		let isUnique = false;

		while (!isUnique) {
			id = '';
			for (let i = 0; i < 15; i++) {
				id += characters.charAt(Math.floor(Math.random() * characters.length));
			}

			// Check if the generated ID already exists
			const existingItem = await pb.collection('items').getFirstListItem(`id="${id}"`).catch(() => null);
			isUnique = !existingItem;
		}

		return id;
	}

	async function handleSubmit() {
		let id = selectedItem?.id;

		if (!id) {
			id = await generateUniqueId();
		}

		// convert timeSold to ISO string
		const timeSoldISO = timeSold ? new Date(timeSold).toISOString() : null;

		const newItem = { id, name, size, colour, price, timeSold: timeSoldISO };

		const updateFunction = async () => {
			try {
				if (selectedItem?.id) {
					await pb.collection('items').update(selectedItem.id, newItem);
				} else {
					await pb.collection('items').create(newItem);
				}
			} catch (error) {
				console.error('Error updating/creating item:', error);
				// Here you might want to revert the UI change if the database update fails
			}
		};

		updateStyles(newItem);
		hidden = true;

		queueUpdate(updateFunction);
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


		<Label class="space-y-2">
			<span>Sold Date and Time</span>
			<Input
				type="datetime-local"
				name="timeSold"
				class="border font-normal outline-none"
				bind:value={timeSold}

			/>
		</Label>

		<div class="bottom-0 left-0 flex w-full justify-center space-x-4 pb-4 md:absolute md:px-4">
			<Button type="submit" class="w-full">{selectedItem?.id ? 'Update' : 'Add'}</Button>
			<Button color="alternative" class="w-full" on:click={() => (hidden = true)}>
				<CloseOutline />
				Cancel
			</Button>
		</div>
	</div>
</form>