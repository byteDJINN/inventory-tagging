import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request, locals }) => {
    const { email, password } = await request.json();

    try {
        const authData = await locals.pb.collection('users').authWithPassword(email, password);

        if (!authData || !authData.token) {
            return json({ success: false, message: 'Authentication failed. Please try again.' }, { status: 400 });
        }

        // Authentication successful
        return json({ success: true, user: authData.record });
    } catch (err) {
        console.error('Sign-in error:', err);
        return json({ success: false, message: 'An error occurred during sign-in. Please try again.' }, { status: 500 });
    }
};