#!/bin/sh

echo "Waiting for DB..."

#while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
#  sleep 0.1
#done

echo "DB started"

python main.py

exec "$@"