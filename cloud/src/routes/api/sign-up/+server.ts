import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request, locals }) => {
    const { email, password, passwordConfirm } = await request.json();

    try {
        const newUser = await locals.pb.collection('users').create({
            email,
            password,
            passwordConfirm
        });

        await locals.pb.collection('users').requestVerification(email);

        return json({ success: true, user: newUser });
    } catch (err) {
        console.error('Sign-up error:', err);
        return json({ success: false, message: 'An error occurred during sign-up. Please try again.' }, { status: 500 });
    }
};