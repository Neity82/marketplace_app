#!/bin/sh

docker-compose down
docker rm -f "$(docker ps -a -q)"
docker volume rm "$(docker volume ls -q)"
docker rmi "$(docker image ls -q)" -f