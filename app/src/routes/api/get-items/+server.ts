import { json, type RequestHandler } from '@sveltejs/kit';
import { getAllNumbers } from '$lib/server/database'; // Adjust the import path if needed

export const GET: RequestHandler = async () => {
    try {
        // Retrieve all numbers from the database
        const numbers = getAllNumbers();

        return json(numbers);
    } catch (error) {
        console.error('Error retrieving numbers:', error);
        return json({ error: 'Internal server error' }, { status: 500 });
    }
};
