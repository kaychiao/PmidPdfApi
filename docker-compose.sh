#!/usr/bin/env bash

# Load environment variables
if [ -f .env ]; then
  export $(cat .env | grep -v '^#' | xargs)
fi

# Default environment
ENV=${1:-local}

# Default command
CMD=${2:-up}

# Additional arguments
ARGS=${@:3}

# Run docker-compose with the specified environment file and volume file
docker-compose -f docker-compose.yml -f dockerfiles/$ENV.yml -f dockerfiles/volume.yml $CMD $ARGS