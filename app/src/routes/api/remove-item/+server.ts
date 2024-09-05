import { json, type RequestHandler } from '@sveltejs/kit';
import { removeNumber } from '$lib/server/database'; // You need to implement this function

export const POST: RequestHandler = async ({ request }) => {
    try {
        const { value } = await request.json();

        // Validate input
        if (typeof value !== 'number') {
            return json({ error: 'Invalid input' }, { status: 400 });
        }

        // Remove number from database
        removeNumber(value);

        return json({ success: true });
    } catch (error) {
        console.error('Error removing number:', error);
        return json({ error: 'Internal server error' }, { status: 500 });
    }
};
