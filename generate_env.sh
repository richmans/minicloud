#!/bin/bash
set -eu
random-string()
{
    env LC_CTYPE=C tr -dc "a-zA-Z0-9-_\$\?" < /dev/urandom | head -c 10
}
mkdir -p env
MYSQL_ROOT_PASSWORD=$(random-string)
echo "MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}" > env/maria.env.txt
RABBIT_ROOT_PASSWORD=$(random-string)
echo "RABBITMQ_DEFAULT_USER=root" > env/rabbit.env.txt
echo "RABBITMQ_DEFAULT_PASS=${RABBIT_ROOT_PASSWORD}" >> env/rabbit.env.txt