import { pb } from '$lib/pocketbase';
import { goto } from '$app/navigation';

const publicPages = ['/authentication/sign-in', '/authentication/sign-up', '/authentication/forgot-password'];

export async function checkAuth() {
    if (!publicPages.includes(window.location.pathname) && !pb.authStore.isValid) {
        try {
            await pb.collection('users').authRefresh();
        } catch (err) {
            console.error('Auth refresh failed:', err);
            goto('/authentication/sign-in');
        }
    }
}

export function logout() {
    pb.authStore.clear();
    goto('/authentication/sign-in');
}

