import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
    const response = await resolve(event);

    // Add permissive CORS headers
    response.headers.set('Access-Control-Allow-Origin', '*');
    response.headers.set('Access-Control-Allow-Methods', '*');
    response.headers.set('Access-Control-Allow-Headers', '*');

    // Handle OPTIONS request
    if (event.request.method === 'OPTIONS') {
        return new Response(null, {
            headers: response.headers
        });
    }

    return response;
};