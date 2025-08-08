FROM node:20-alpine

WORKDIR /app

# Install development tools
RUN apk add --no-cache git curl bash

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Development command
CMD ["npm", "run", "dev"]