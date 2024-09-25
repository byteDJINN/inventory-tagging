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

<nav class="bg-blue-600 p-4 text-white">
    <div class="container mx-auto flex justify-between items-center">
        <h1 class="text-2xl font-bold">Dashboard</h1>
    </div>
</nav>

<div class="container mx-auto p-4">
    
    {#if items.length === 0}
        <div class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4" role="alert">
            <p>No items found in the inventory. Add some items to get started!</p>
        </div>
    {:else}
        <div class="overflow-x-auto">
            <table class="min-w-full bg-white shadow-md rounded-lg overflow-hidden">
                <thead class="bg-gray-100">
                    <tr>
                        <th class="px-4 py-2 text-left">ID</th>
                        <th class="px-4 py-2 text-left">Name</th>
                        <th class="px-4 py-2 text-left">Quantity</th>
                    </tr>
                </thead>
                <tbody>
                    {#each items as item}
                        <tr class="border-b hover:bg-gray-50">
                            <td class="px-4 py-2">{item.id}</td>
                            <td class="px-4 py-2">{item.name}</td>
                            <td class="px-4 py-2">{item.tags.length}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
</div>