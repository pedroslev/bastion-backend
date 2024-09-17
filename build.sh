#!/bin/bash

# Define variables
IMAGE_NAME="pedroslev/bastion-backend"
VERSION="v5.0.0"

# Build the Docker image
docker build --platform linux/amd64 -t ${IMAGE_NAME}:${VERSION} . | tee build.log || exit 1
ID=$(tail -1 build.log | awk '{print $3;}')
# Tag the Docker image
docker tag $ID ${IMAGE_NAME}:${VERSION}


# Log in to Docker Hub
docker login --username=pedroslev --password='labradora1M'

# Push the Docker image to Docker Hub
docker push ${IMAGE_NAME}:${VERSION}

# Output the image name for verification
echo "Docker image pushed to Docker Hub: ${IMAGE_NAME}:${VERSION}"
