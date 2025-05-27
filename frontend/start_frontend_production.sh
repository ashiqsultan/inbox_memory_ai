#!/bin/bash

# This script should be run in the production environment server

# Stop and remove existing container if it exists
if [ "$(docker ps -q -f name=inbox-memory-frontend)" ]; then
    echo "Stopping existing container..."
    docker stop inbox-memory-frontend
    docker rm inbox-memory-frontend
fi

# Build the Docker image
echo "Building Docker image..."
docker build -t inbox-memory-frontend-vite-app .

# Run the container in background
echo "Starting container..."
docker run -d \
    --name inbox-memory-frontend \
    -p 5100:80 \
    --restart unless-stopped \
    inbox-memory-frontend-vite-app

echo "Deployment completed! Container is running in background on port 3001" 