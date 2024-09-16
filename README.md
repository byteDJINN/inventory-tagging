## Quick Commands
```bash
cd app
docker-compose up --build
```

```bash
cd device
docker-compose run --build device
```

## Architecture

Docker will be used for development. This allows everyone to run the code within the same environment and not have to install any dependencies. 

### Raspberry Pi 

This will read data from the sensors (scanner and camera). 

It will run a flask server locally creating a UI for use when scanning. We will connect the RPi to a monitor allowing the user to view the localhost UI webpage from the RPi. 

A user may take a photo of a tag, then scan some number of RFID tags, as they scan them they may appear on the webpage, and when they are finished they can submit them using a button the website, where they are pushed (via the cloud server) into the inventory database. 

The RPi will need internet access (WiFi) since it will send requests to the server through GET/POST URL requests. 

### Server

This is the cloud analytics and database for the service. It will host a website which can show all the inventory and allow searching through it. 

It will have a database storing all the information about items including their names and RFID tag IDs. 

It will also have some API routes for the RPi (device) service to use to update the database. For example, there may be a route to add a bunch of items into the database, and another route to mark some items as sold.

#### SvelteKit

The server will be a single SvelteKit process. SvelteKit is a fullstack (frontend and backend) framework designed for simplicity. 

Interactive tutorial: https://learn.svelte.dev/tutorial/welcome-to-svelte

#### SQLite

We will use a SQLite database to store information. 

#### HTML, TypeScript, and TailwindCSS

The original website stack is "HTML, JavaScript, and CSS". However, there are some modern frameworks that will make development simpler. 

Rather than using JavaScript we will use TypeScript, it's almost identical but more commonly used and less likely to have bugs. 

Instead of CSS, we will use TailwindCSS. TailwindCSS is a collection of pre-made CSS classes, so we won't have to design any ourselves. 

TailwindCSS Documentation: https://tailwindcss.com/docs/utility-first 

## Raspberry Pi

`device` has the code for the Raspberry Pi. 

`docker-compose run --build device` gives an interactive shell.

You will be able to add and edit all the files in VSCode, and they will automatically change within the container. 

## Server

`app` has the code for the frontend/backend/database. 

Important paths
```
db.sqlite
/src
    /lib
        /server
            database.ts
    /routes
        /api
            /add-item
            /get-items
            /remove-item
        +page.svelte
```

### Running

First you need to add a .env.ts file in /app/src/lib/server with the following:
```
export const OPENAI_API_KEY = "...";
```

To run, use `docker-compose up --build` from within `/app`. This will take longer the first time. Once it is running you should be able to change any code and it will auto update instantly. 
