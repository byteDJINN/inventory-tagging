<script lang="ts">

    import { onMount } from 'svelte';
    
    let items: string[] = [];

    onMount(async () => {
        // request its own url /api
        const res = await fetch('/api/get-items');
        items = await res.json();
        
        console.log(items);
    });
    
</script>


<div class="mx-2">
    <ul>
        {#each items as item}
            <li>{item}</li>
        {/each}
    </ul>
</div>
