# Smart Inventory Tagging

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

To run, use `docker-compose up --build`. This will take longer the first time. Once it is running you should be able to change any code and it will auto update instantly. 


Testing the routes that the RPi will use to send and receive information. 
```bash

# adds another item
curl -X POST http://localhost:5173/api/add-item -H "Content-Type: application/json" -d '{"value": 42}'

# returns all the items
curl http://localhost:5173/api/get-items
```