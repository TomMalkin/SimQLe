#!/usr/bin/zsh

docker-compose down
docker-compose up --abort-on-container-exit --exit-code-from tester --build
