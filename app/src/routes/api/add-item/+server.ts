import { json, type RequestHandler } from '@sveltejs/kit';
import { addItem } from '$lib/server/database'; // Adjust the import path if needed

export const POST: RequestHandler = async ({ request }: { request: Request }) => {
    try {
        const { base64Image, tags } = await request.json();

        // Validate input
        if (typeof base64Image !== 'string' || !Array.isArray(tags)) {
            return json({ error: 'Invalid input' }, { status: 400 });
        }

        // Add number to database
        await addItem(base64Image, tags);

        return json({ success: true });
    } catch (error) {
        console.error('Error adding item:', error);
        return json({ error: 'Internal server error' }, { status: 500 });
    }
};


