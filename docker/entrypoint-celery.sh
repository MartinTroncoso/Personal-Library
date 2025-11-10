#!/bin/sh
set -e

echo "📡 Waiting for data base to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "✅ Data base ready."

echo "🔍 Waiting for the django_celery_beat migrations to be applied..."

until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT 1 FROM django_migrations WHERE app='django_celery_beat' AND name='0001_initial';" \
  | grep -q 1; do
  echo "⏳ django_celery_beat migrations not applied yet. Waiting..."
  sleep 2
done

echo "✅ django_celery_beat migrations detected."

exec "$@"

