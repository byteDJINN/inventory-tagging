# Dockerfile

# Use the official Node.js image.
FROM node:lts-alpine

# Set the working directory.
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your app's source code
COPY . .

ENV NODE_OPTIONS=--max_old_space_size=4096

# Build the SvelteKit app
RUN npm run build

# Expose the port your SvelteKit app will run on
EXPOSE 3003

# Set the HOST and PORT environment variables
ENV HOST=0.0.0.0
ENV PORT=3003


# Start the server using the production build
CMD ["node", "build"]