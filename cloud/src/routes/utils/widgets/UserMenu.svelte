<script lang="ts">
	import { imagesPath } from '../../utils/variables';
	import { Avatar, Dropdown, DropdownDivider, DropdownHeader, DropdownItem } from 'flowbite-svelte';
	import { goto } from '$app/navigation';
	import { pb } from '$lib/pocketbase';
	import { invalidateAll } from '$app/navigation';
	
	// Add this import for the user icon
	import { UserCircleSolid } from 'flowbite-svelte-icons';

	export let user: any = null;
	
	function handleDashboard() {
		goto('/dashboard');
	}

	async function handleSignOut() {
		try {
			const response = await fetch('/api/sign-out', { method: 'POST' });
			const result = await response.json();

			if (result.success) {
				pb.authStore.clear();
				await invalidateAll();
				goto('/authentication/sign-in');
			} else {
				console.error('Sign out failed:', result.message);
			}
		} catch (error) {
			console.error('Sign out error:', error);
		}
	}
</script>
<button class="ms-3 rounded-full dark:ring-gray-600">
		<UserCircleSolid class="w-6 h-6 text-gray-500 dark:text-gray-400" />
</button>
<Dropdown placement="bottom-end">
	<DropdownHeader>
		<span class="block text-sm">{user.email}</span>
	</DropdownHeader>
	<DropdownItem on:click={handleDashboard}>Dashboard</DropdownItem>
	<DropdownItem on:click={handleSignOut}>Sign out</DropdownItem>
</Dropdown>

<!--
@component
[Go to docs](https://flowbite-svelte-admin-dashboard.vercel.app/)
## Props
@prop export let id: number = 0;
@prop export let name: string = '';
@prop export let avatar: string = '';
@prop export let email: string = '';
@prop export let biography: string = '';
@prop export let position: string = '';
@prop export let country: string = '';
@prop export let status: string = '';
-->
