import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ locals }) => {
    locals.pb.authStore.clear();
    return json({ success: true, message: 'Signed out successfully' });
};