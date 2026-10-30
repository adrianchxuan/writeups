#!/bin/sh
set -e

if [ -d /app/storage.seed ]; then
  cp -r /app/storage.seed/. /app/storage/
fi

exec "$@"
