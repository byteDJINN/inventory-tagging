<script lang="ts">
	import { Button, CloseButton, Heading, Input, Label, Textarea } from 'flowbite-svelte';
	import { CloseOutline } from 'flowbite-svelte-icons';
	import { createEventDispatcher } from 'svelte';
	import { pb } from '$lib/pocketbase';

	export let hidden: boolean = true;
	export let selectedStyle: any = null;

	const dispatch = createEventDispatcher();

	let name: string = selectedStyle?.name || '';
	let description: string = selectedStyle?.description || '';

	async function handleSubmit() {
		try {
			if (selectedStyle) {
				await pb.collection('style').update(selectedStyle.id, { name, description });
			} else {
				await pb.collection('style').create({ name, description });
			}
			dispatch('styleUpdated');
		} catch (error) {
			console.error('Error updating/creating style:', error);
		}
	}
</script>

<Heading tag="h5" class="mb-6 text-sm font-semibold uppercase">
	{selectedStyle ? 'Update style' : 'Add new style'}
</Heading>
<CloseButton
	on:click={() => (hidden = true)}
	class="absolute right-2.5 top-2.5 text-gray-400 hover:text-black dark:text-white"
/>

<form on:submit|preventDefault={handleSubmit}>
	<div class="space-y-4">
		<Label class="space-y-2">
			<span>Name</span>
			<Input
				name="name"
				class="border font-normal outline-none"
				placeholder="Enter style name"
				required
				bind:value={name}
			/>
		</Label>

		<Label class="space-y-2">
			<span>Description</span>
			<Textarea
				name="description"
				class="border font-normal outline-none"
				placeholder="Enter style description"
				required
				bind:value={description}
			/>
		</Label>

		<div class="bottom-0 left-0 flex w-full justify-center space-x-4 pb-4 md:absolute md:px-4">
			<Button type="submit" class="w-full">{selectedStyle ? 'Update' : 'Add'}</Button>
			<Button color="alternative" class="w-full" on:click={() => (hidden = true)}>
				<CloseOutline />
				Cancel
			</Button>
		</div>
	</div>
</form>