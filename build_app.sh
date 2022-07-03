#!/bin/sh

DOCKER_COMPOSE_FILE="./docker-compose.yml"

docker-compose -f "$DOCKER_COMPOSE_FILE" down -v
docker-compose -f "$DOCKER_COMPOSE_FILE" build
docker-compose -f "$DOCKER_COMPOSE_FILE" up

