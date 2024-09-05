import { json, type RequestHandler } from '@sveltejs/kit';
import { addNumber } from '$lib/server/database'; // Adjust the import path if needed

export const POST: RequestHandler = async ({ request }) => {
    try {
        const { value } = await request.json();

        // Validate input
        if (typeof value !== 'number') {
            return json({ error: 'Invalid input' }, { status: 400 });
        }

        // Add number to database
        addNumber(value);

        return json({ success: true });
    } catch (error) {
        console.error('Error adding number:', error);
        return json({ error: 'Internal server error' }, { status: 500 });
    }
};
