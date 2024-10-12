<script lang="ts">
	import { Label, Input, Alert } from 'flowbite-svelte';
	import SignIn from '../utils/authentication/SignIn.svelte';
	import { pb } from '$lib/pocketbase';
	import { goto } from '$app/navigation';

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
			const authData = await pb.collection('users').authWithPassword(email, password);
			
			if (authData.record.verified) {
				goto('/dashboard'); // Redirect to dashboard or home page
			} else {
				errorMessage = 'Please verify your email before logging in. Check your inbox for the verification link.';
			}
		} catch (err) {
			console.error('Error:', err);
			errorMessage = 'Invalid email or password';
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
