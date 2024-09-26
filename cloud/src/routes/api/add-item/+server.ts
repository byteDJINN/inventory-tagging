import { json, type RequestHandler } from '@sveltejs/kit';
import { addItem } from '$lib/server/database'; // Adjust the import path if needed

export const POST: RequestHandler = async ({ request }: { request: Request }) => {
    try {
        const { name, tags } = await request.json();

        // Add number to database
        await addItem(name, tags);

        return json({ success: true });
    } catch (error) {
        console.error('Error adding item:', error);
        return json({ error: 'Internal server error' }, { status: 500 });
    }
};


export const OPTIONS: RequestHandler = () => new Response(null);