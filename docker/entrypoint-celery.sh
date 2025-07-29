#!/bin/sh
set -e

echo "📡 Esperando a la base de datos..."
while ! nc -z db 5432; do
  sleep 1
done
echo "✅ Base de datos lista."

echo "🔍 Esperando a que se apliquen las migraciones de django_celery_beat..."

until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT 1 FROM django_migrations WHERE app='django_celery_beat' AND name='0001_initial';" \
  | grep -q 1; do
  echo "⏳ Migraciones de django_celery_beat aún no aplicadas. Esperando..."
  sleep 2
done

echo "✅ Migraciones de django_celery_beat detectadas."

exec "$@"