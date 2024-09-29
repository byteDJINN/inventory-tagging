<script lang="ts">
	import { Label, Input, Alert } from 'flowbite-svelte';
	import ResetPassword from '../utils/authentication/ResetPassword.svelte';
	import { pb } from '$lib/pocketbase';
	import { goto } from '$app/navigation';

	const title = 'Reset your password';
	const site = {
		name: 'Flowbite',
		img: '/images/flowbite-svelte-icon-logo.svg',
		link: '/',
		imgAlt: 'FlowBite Logo'
	};
	const acceptTerms = true;
	const btnTitle = 'Reset password';
	const termsLink = '/';
	const labelClass = 'mb-2 dark:text-white';
	const inputClass = 'border outline-none dark:border-gray-600 dark:bg-gray-700';

	let password = '';
	let confirmPassword = '';
	let errorMessage = '';

	// Get token and user ID from URL parameters
	const urlParams = new URLSearchParams(window.location.search);
	const token = urlParams.get('token');
	const userId = urlParams.get('userId');

	const onSubmit = async (e: Event) => {
		e.preventDefault();
		errorMessage = '';

		if (password !== confirmPassword) {
			errorMessage = 'Passwords do not match';
			return;
		}

		try {
			await pb.collection('users').confirmPasswordReset(
				token,
				password,
				confirmPassword
			);
			goto('/authentication/sign-in'); // Redirect to sign-in page
		} catch (err) {
			console.error('Error:', err);
			errorMessage = 'An error occurred. Please try again.';
		}
	};
	
</script>

<ResetPassword {title} {site} {acceptTerms} {btnTitle} {termsLink} on:submit={onSubmit}>
	{#if errorMessage}
		<Alert color="red" class="mb-4">{errorMessage}</Alert>
	{/if}
	<div>
		<Label for="password" class={labelClass}>New password</Label>
		<Input
			type="password"
			name="password"
			id="password"
			bind:value={password}
			placeholder="••••••••"
			required
			class={inputClass}
		/>
	</div>
	<div>
		<Label for="confirm-password" class={labelClass}>Confirm new password</Label>
		<Input
			type="password"
			name="confirm-password"
			id="confirm-password"
			bind:value={confirmPassword}
			placeholder="••••••••"
			required
			class={inputClass}
		/>
	</div>
</ResetPassword>
