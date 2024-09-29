<script lang="ts">
    import { Alert, Input, Button } from 'flowbite-svelte';
    import { pb } from '$lib/pocketbase';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    let message = 'Please enter the verification code sent to your email.';
    let isError = false;
    let verificationCode = '';
    let email = '';

    onMount(() => {
        const urlParams = new URLSearchParams(window.location.search);
        email = urlParams.get('email') || '';
    });

    async function verifyEmail() {
        if (!verificationCode) {
            message = 'Please enter the verification code.';
            isError = true;
            return;
        }

        try {
            await pb.collection('users').confirmVerification(verificationCode);
            message = 'Email verified successfully. You can now log in.';
            isError = false;
            setTimeout(() => goto('/authentication/sign-in'), 3000);
        } catch (err) {
            console.error('Error:', err);
            message = 'Failed to verify email. Please check the code and try again.';
            isError = true;
        }
    }
</script>

<div class="flex justify-center items-center h-screen">
    <div class="max-w-md w-full space-y-4">
        <Alert color={isError ? 'red' : 'blue'}>
            {message}
        </Alert>
        <Input
            type="text"
            placeholder="Enter verification code"
            bind:value={verificationCode}
        />
        <Button on:click={verifyEmail} class="w-full">
            Verify Email
        </Button>
    </div>
</div>