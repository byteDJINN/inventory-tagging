<script lang="ts">
	import { Button, CloseButton, Heading, Input, Label, Select } from 'flowbite-svelte';
	import { CloseOutline } from 'flowbite-svelte-icons';
	import { createEventDispatcher } from 'svelte';
	import { pb } from '$lib/pocketbase';

	export let hidden: boolean = true;
	export let selectedAttribute: any = null;

	const dispatch = createEventDispatcher();

	let type: string = selectedAttribute?.type || '';
	let value: string = selectedAttribute?.value || '';

	async function handleSubmit() {
		try {
			if (selectedAttribute) {
				await pb.collection('attribute').update(selectedAttribute.id, { type, value });
			} else {
				await pb.collection('attribute').create({ type, value });
			}
			dispatch('attributeUpdated');
		} catch (error) {
			console.error('Error updating/creating attribute:', error);
		}
	}
</script>

<Heading tag="h5" class="mb-6 text-sm font-semibold uppercase">
	{selectedAttribute ? 'Update attribute' : 'Add new attribute'}
</Heading>
<CloseButton
	on:click={() => (hidden = true)}
	class="absolute right-2.5 top-2.5 text-gray-400 hover:text-black dark:text-white"
/>

<form on:submit|preventDefault={handleSubmit}>
	<div class="space-y-4">
		<Label class="space-y-2">
			<span>Type</span>
			<Input
				name="type"
				class="border font-normal outline-none"
				placeholder="Enter attribute type"
				required
				bind:value={type}
			/>
		</Label>

		<Label class="space-y-2">
			<span>Value</span>
			<Input
				name="value"
				class="border font-normal outline-none"
				placeholder="Enter attribute value"
				required
				bind:value={value}
			/>
		</Label>

		<div class="bottom-0 left-0 flex w-full justify-center space-x-4 pb-4 md:absolute md:px-4">
			<Button type="submit" class="w-full">{selectedAttribute ? 'Update' : 'Add'}</Button>
			<Button color="alternative" class="w-full" on:click={() => (hidden = true)}>
				<CloseOutline />
				Cancel
			</Button>
		</div>
	</div>
</form>
