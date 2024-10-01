# Dockerfile

# Use the official Node.js image.
FROM node:lts-alpine

# Set the working directory.
WORKDIR /app

COPY package.json ./

RUN npm install

# Copy the rest of your app's source code.
COPY . .

# Expose the port your SvelteKit app will run on.
EXPOSE 3003

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]