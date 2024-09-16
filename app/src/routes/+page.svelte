<script lang="ts">
    import { onMount } from 'svelte';

    interface Item {
        id: number;
        name: string;
        tags: { id: number }[];
    }

    let items: Item[] = [];

    onMount(async () => {
        const res = await fetch('/api/get-items');
        items = await res.json();
        console.log(items);
    });
</script>

<div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Inventory Items</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {#each items as item}
            <div class="bg-white shadow-md rounded-lg overflow-hidden flex flex-col">
                <div class="p-4 flex-grow">
                    <h2 class="text-xl font-semibold">{item.name}</h2>
                </div>
                <div class="p-4 mt-auto flex justify-between items-center">
                    <span class="text-smfont-bold">Quantity:</span>
                    <span class="text-md font-bold">{item.tags.length}</span>
                </div>
            </div>
        {/each}
    </div>
</div>