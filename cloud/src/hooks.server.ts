import PocketBase from 'pocketbase';
import { env } from '$env/dynamic/private'
import type { Handle } from '@sveltejs/kit';
import { sequence } from '@sveltejs/kit/hooks';
import { redirect } from '@sveltejs/kit';

export const authentication: Handle = async ({ event, resolve }) => {
    event.locals.pb = new PocketBase("https://inventory.bytedjinn.com/db/");

    // load the store data from the request cookie string
    event.locals.pb.authStore.loadFromCookie(event.request.headers.get('cookie') || '');

    try {
        // get an up-to-date auth store state by verifying and refreshing the loaded auth model (if any)
        event.locals.pb.authStore.isValid && await event.locals.pb.collection('users').authRefresh();
    } catch (_) {
        // clear the auth store on failed refresh
        event.locals.pb.authStore.clear();
    }

    const response = await resolve(event);

    // send back the default 'pb_auth' cookie to the client with the latest store state
    response.headers.append('set-cookie', event.locals.pb.authStore.exportToCookie());

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
}

const unprotectedRoutes = ['/authentication', '/api/sign-in', '/api/sign-up', '/api/sign-out'];
export const authorization: Handle = async ({ event, resolve }) => {

    if (!unprotectedRoutes.some(route => event.url.pathname.startsWith(route))) {

        const loggedIn = await event.locals.pb.authStore.isValid;

        if (!loggedIn) {
            throw redirect(303, '/authentication/sign-in');
        }
    }

    // If the request is still here, just proceed as normally

    const result = await resolve(event);
    return result;
};

export const handle = sequence(authentication, authorization)

