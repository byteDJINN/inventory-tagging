import { json, type RequestHandler } from '@sveltejs/kit';
import { getAllItems } from '$lib/server/database'; // Adjust the import path if needed

export const GET: RequestHandler = async () => {
    try {
        // Retrieve all items from the database
        const items = await getAllItems();

        return json(items);
    } catch (error) {
        console.error('Error retrieving items:', error);
        return json({ error: 'Internal server error' }, { status: 500 });
    }
};
