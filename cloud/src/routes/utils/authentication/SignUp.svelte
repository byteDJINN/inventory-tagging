<script lang="ts">
	import { A, Checkbox, Button, Card } from 'flowbite-svelte';
	export let title = 'Create a Free Account';
	export let haveAccount: boolean = true;
	export let btnTitle = 'Create account';
	export let loginLink = '/';
	export let mainClass = 'bg-gray-50 dark:bg-gray-900 w-full';
	export let mainDivClass =
		'flex flex-col items-center justify-center px-6 pt-8 mx-auto md:h-screen pt:mt-0 dark:bg-gray-900';
	export let cardH1Class = 'text-2xl font-bold text-gray-900 dark:text-white';
	export let haveAccountDivClass = 'text-sm font-medium text-gray-500 dark:text-gray-400';
</script>

<main class={mainClass}>
	<div class={mainDivClass}>
		<!-- Card -->
		<Card class="w-full" size="md" border={false}>
			<h1 class={cardH1Class}>
				{title}
			</h1>
			<form class="mt-8 space-y-6" on:submit|preventDefault>
				<slot />
				<Button type="submit" size="lg">{btnTitle}</Button>
				{#if haveAccount}
					<div class={haveAccountDivClass}>
						Already have an account? <A href={loginLink}>Login here</A>
					</div>
				{/if}
			</form>
		</Card>
	</div>
</main>
