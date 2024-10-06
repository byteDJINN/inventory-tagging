<script lang="ts">
	import { Button, Card, P } from 'flowbite-svelte';
	export let title = 'Forgot your password?';
	export let btnTitle = 'Reset password';
	export let pageDescription =
		"Don't fret! Just type in your email and we will send you a code to reset your password!";
	export let mainClass = 'bg-gray-50 dark:bg-gray-900';
	export let mainDivClass =
		'flex flex-col items-center justify-center px-6 pt-8 mx-auto md:h-screen pt:mt-0 dark:bg-gray-900';
	export let cardH1Class = 'mb-3 text-2xl font-bold text-gray-900 dark:text-white';
</script>

<main class={mainClass}>
	<div class={mainDivClass}>
		<!-- Card -->
		<Card class="w-full max-w-md" border={false}>
			<h1 class={cardH1Class}>{title}</h1>
			<P class="text-base font-normal text-gray-500 dark:text-gray-400">
				{pageDescription}
			</P>
			<form class="mt-8 space-y-6" on:submit|preventDefault>
				<slot />
				<Button type="submit" size="lg">{btnTitle}</Button>
			</form>
		</Card>
	</div>
</main>
