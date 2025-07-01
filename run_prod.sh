#!/usr/bin/env bash

# Load environment variables
if [ -f .env ]; then
  export $(cat .env | grep -v '^#' | xargs)
fi

# Ensure network exists
docker network create pmid-pdf-api-nw || true

# Stop any running containers
docker-compose -f docker-compose.yml -f dockerfiles/prod.yml -f dockerfiles/volume.yml down

# Build and start containers
docker-compose -f docker-compose.yml -f dockerfiles/prod.yml -f dockerfiles/volume.yml up -d