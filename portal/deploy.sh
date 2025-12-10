#!/bin/bash

# DeepSonar Deployment Script

APP_NAME="deepsonar-app"
PORT=3001

echo "🚀 Starting deployment for $APP_NAME..."

# 1. Pull latest changes (optional, uncomment if running on server via git)
# git pull origin main

# 2. Build Docker Image
echo "📦 Building Docker image..."
docker build -t $APP_NAME .

# 3. Stop running container (if any)
if [ "$(docker ps -q -f name=$APP_NAME)" ]; then
    echo "🛑 Stopping existing container..."
    docker stop $APP_NAME
    docker rm $APP_NAME
fi

# 4. Run new container
echo "▶️ Starting new container..."
docker run -d \
  --name $APP_NAME \
  -p $PORT:3001 \
  --restart unless-stopped \
  -e NODE_ENV=production \
  $APP_NAME

echo "✅ Deployment complete! App is running on port $PORT"
