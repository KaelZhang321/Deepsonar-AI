# Stage 1: Build the frontend
FROM node:20-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY server/package*.json ./server/

# Install dependencies (including devDependencies for build)
RUN npm install
# Install server dependencies specifically
RUN cd server && npm install

# Copy source code
COPY . .

# Build the frontend
RUN npm run build

# Stage 2: Serve with Node.js
FROM node:20-alpine

WORKDIR /app

# Copy server dependencies
COPY --from=build /app/server/node_modules ./server/node_modules
COPY --from=build /app/server/package.json ./server/

# Copy built frontend assets
COPY --from=build /app/dist ./dist

# Copy server code
COPY --from=build /app/server/index.js ./server/

# Expose the API port
EXPOSE 3001

# Start the server
WORKDIR /app/server
CMD ["npm", "start"]
