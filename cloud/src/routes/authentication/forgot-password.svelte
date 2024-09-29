<script lang="ts">
	import ForgotPassword from '../utils/authentication/ForgotPassword.svelte';
	import { Label, Input, Alert } from 'flowbite-svelte';
	import { pb } from '$lib/pocketbase';

	let email = '';
	let successMessage = '';
	let errorMessage = '';

	const onSubmit = async (e: Event) => {
		e.preventDefault();
		successMessage = '';
		errorMessage = '';

		try {
			await pb.collection('users').requestPasswordReset(email);
			successMessage = 'Password reset instructions have been sent to your email.';
		} catch (err) {
			console.error('Error:', err);
			errorMessage = 'An error occurred. Please try again.';
		}
	};
</script>

<ForgotPassword on:submit={onSubmit}>
	{#if successMessage}
		<Alert color="green" class="mb-4">{successMessage}</Alert>
	{/if}
	{#if errorMessage}
		<Alert color="red" class="mb-4">{errorMessage}</Alert>
	{/if}
	<div>
		<Label for="email" class="mb-2">Your email</Label>
		<Input
			type="email"
			name="email"
			id="email"
			bind:value={email}
			placeholder="name@company.com"
			required
			class="border outline-none"
		/>
	</div>
</ForgotPassword>
