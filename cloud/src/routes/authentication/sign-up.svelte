<script lang="ts">
	import { Label, Input, Alert } from 'flowbite-svelte';
	import SignUp from '../utils/authentication/SignUp.svelte';
	import { pb } from '$lib/pocketbase';
	import { goto, invalidateAll } from '$app/navigation';

	const title = 'Create a Free Account';
	const site = {
		name: 'Flowbite',
		img: '/images/flowbite-svelte-icon-logo.svg',
		link: '/',
		imgAlt: 'FlowBite Logo'
	};
	const acceptTerms = true;
	const haveAccount = true;
	const btnTitle = 'Create account';
	const termsLink = '/';
	const loginLink = 'sign-in';
	const labelClass = 'space-y-2 dark:text-white';

	let email = '';
	let password = '';
	let passwordConfirm = '';
	let errorMessage = '';
	let successMessage = '';

	const onSubmit = async (e: Event) => {
		e.preventDefault();
		errorMessage = '';
		successMessage = '';

		if (password !== passwordConfirm) {
			errorMessage = 'Passwords do not match';
			return;
		}

		try {
			const response = await fetch('/api/sign-up', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password, passwordConfirm })
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.message || 'An error occurred during sign up');
			}

			const result = await response.json();

			if (result.success) {
				successMessage = 'Account created successfully. Please check your email to verify your account before signing in.';
				// Optionally, you can redirect to the sign-in page after a short delay
				setTimeout(() => goto('/authentication/sign-in'), 5000);
			} else {
				errorMessage = result.message || 'An error occurred during sign up';
			}
		} catch (err) {
			console.error('Error:', err);
			errorMessage = err.message || 'An error occurred during sign up';
		}
	};
</script>

<SignUp
	{title}
	{site}
	{acceptTerms}
	{haveAccount}
	{btnTitle}
	{termsLink}
	{loginLink}
	on:submit={onSubmit}
>
	{#if errorMessage}
		<Alert color="red" class="mb-4">{errorMessage}</Alert>
	{/if}
	{#if successMessage}
		<Alert color="green" class="mb-4">{successMessage}</Alert>
	{/if}
	<div>
		<Label class={labelClass}>
			<span>Your email</span>
			<Input
				type="email"
				name="email"
				bind:value={email}
				placeholder="name@company.com"
				required
				class="border outline-none dark:border-gray-600 dark:bg-gray-700"
			/>
		</Label>
	</div>
	<div>
		<Label class={labelClass}>
			<span>Your password</span>
			<Input
				type="password"
				name="password"
				bind:value={password}
				placeholder="••••••••"
				required
				class="border outline-none dark:border-gray-600 dark:bg-gray-700"
			/>
		</Label>
	</div>
	<div>
		<Label class={labelClass}>
			<span>Confirm password</span>
			<Input
				type="password"
				name="confirm-password"
				bind:value={passwordConfirm}
				placeholder="••••••••"
				required
				class="border outline-none dark:border-gray-600 dark:bg-gray-700"
			/>
		</Label>
	</div>
</SignUp>
