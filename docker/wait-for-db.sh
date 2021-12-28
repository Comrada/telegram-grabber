#!/bin/bash
set -e

until timeout 1 bash -c "cat < /dev/null > /dev/tcp/${DB_HOST}/${DB_PORT}"; do
  >&2 echo "PostgreSQL not up yet on ${DB_HOST}"
  sleep 5
done

echo "PostgreSQL is up"
exec "$@"
