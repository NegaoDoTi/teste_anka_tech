#!/bin/sh
set -e

until nc -z db 5432; do
  sleep 1
done

until nc -z rabbitmq 5672; do
  sleep 1
done

alembic upgrade head

python app.py &

python run.py &

wait
