<script lang="ts">
	import { Label, Input, Alert } from 'flowbite-svelte';
	import SignIn from '../utils/authentication/SignIn.svelte';
	import { goto, invalidateAll } from '$app/navigation';

	let title = 'Sign in to platform';
	let site = {
		name: 'Flowbite',
		img: '/images/flowbite-svelte-icon-logo.svg',
		link: '/',
		imgAlt: 'FlowBite Logo'
	};
	let rememberMe = true;
	let lostPassword = true;
	let createAccount = true;
	let lostPasswordLink = 'forgot-password';
	let loginTitle = 'Login to your account';
	let registerLink = 'sign-up';
	let createAccountTitle = 'Create account';

	let email = '';
	let password = '';
	let errorMessage = '';

	const onSubmit = async (e: Event) => {
		e.preventDefault();
		errorMessage = '';

		try {
			console.log('Attempting to sign in...');
			const response = await fetch('/api/sign-in', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password })
			});

			console.log('Response status:', response.status);
			
			if (!response.ok) {
				const responseText = await response.text();
				console.error('Response text:', responseText);
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const result = await response.json();
			console.log('Sign-in result:', result);

			if (result.success) {
				console.log('Auth successful, user:', result.user);
				await invalidateAll();
				goto('/dashboard');
			} else {
				errorMessage = result.message || 'Authentication failed';
			}
		} catch (err) {
			console.error('Sign-in error:', err);
			errorMessage = 'An error occurred during sign-in. Please try again.';
		}
	};
</script>

<SignIn
	{title}
	{site}
	{rememberMe}
	{lostPassword}
	{createAccount}
	{lostPasswordLink}
	{loginTitle}
	{registerLink}
	{createAccountTitle}
	on:submit={onSubmit}
>
	{#if errorMessage}
		<Alert color="red" class="mb-4">{errorMessage}</Alert>
	{/if}
	<div>
		<Label for="email" class="mb-2 dark:text-white">Your email</Label>
		<Input
			type="email"
			name="email"
			id="email"
			bind:value={email}
			placeholder="name@company.com"
			required
			class="border outline-none dark:border-gray-600 dark:bg-gray-700"
		/>
	</div>
	<div>
		<Label for="password" class="mb-2 dark:text-white">Your password</Label>
		<Input
			type="password"
			name="password"
			id="password"
			bind:value={password}
			placeholder="••••••••"
			required
			class="border outline-none dark:border-gray-600 dark:bg-gray-700"
		/>
	</div>
</SignIn>
