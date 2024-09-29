// src/routes/components/[slug]/+page.js
/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
	const post = await import(`../${params.slug}.svelte`);
	// const { title, dir } = post.metadata;
	const content = post.default;

	let r1;

	fetch('http://localhost:9876/api/button-count')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        r1 = data;
        console.log("@@@",r1); // Output the result
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });


	return {
		content,
		params:params.slug
		// title,
		// dir
	};
}
