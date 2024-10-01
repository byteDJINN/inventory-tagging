<script lang="ts">
    import { MultiSelect } from 'flowbite-svelte';
    import { onMount } from 'svelte';

    export let hidden: boolean;
    export let drawerItem: any;
    export let availableAttributes: string[];
    export let updateItemAttributes: (itemId: string, selection: {name: string, value: string}[]) => Promise<void>;

    let selectedAttributes: string[] = drawerItem.attributes || [];
    export let updateQueue: (() => Promise<void>)[];
    export let queueUpdate;




    // Watch for changes in selectedAttributes
    $: {
        if (selectedAttributes) {
            queueUpdate(selectedAttributes);
        }
    }

    onMount(() => {
        // Initial update if necessary
        if (selectedAttributes.length > 0) {
            queueUpdate(selectedAttributes);
        }
    });
</script>

<div class="p-4">
    <h2 class="mb-4 text-2xl font-bold">Edit Attributes for {drawerItem.tagID}</h2>
    <MultiSelect
        items={availableAttributes.map(attr => ({ value: attr, name: attr }))}
        bind:value={selectedAttributes}
        class="mb-4 text-xs"
        textSize="text-xs sm:text-xs"
    />
</div>
