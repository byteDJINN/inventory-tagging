<script lang="ts">
	import { Label, Input, Alert } from 'flowbite-svelte';
	import SignUp from '../utils/authentication/SignUp.svelte';
	import { pb } from '$lib/pocketbase';
	import { goto } from '$app/navigation';

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
	let confirmPassword = '';
	let errorMessage = '';

	const onSubmit = async (e: Event) => {
		e.preventDefault();
		errorMessage = '';

		if (password !== confirmPassword) {
			errorMessage = 'Passwords do not match';
			return;
		}

		try {
			const user = await pb.collection('users').create({
				email,
				password,
				passwordConfirm: confirmPassword,
			});
			
			await pb.collection('users').requestVerification(email);
			
			goto('/authentication/verify-email?email=' + encodeURIComponent(email));
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
				bind:value={confirmPassword}
				placeholder="••••••••"
				required
				class="border outline-none dark:border-gray-600 dark:bg-gray-700"
			/>
		</Label>
	</div>
</SignUp>
