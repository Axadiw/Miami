#!/bin/sh

docker network create webproxy --driver overlay --attachable
docker stack deploy -c nginx-letsencrypt-swarm.yml nginx-proxy