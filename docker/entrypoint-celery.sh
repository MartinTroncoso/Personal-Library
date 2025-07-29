#!/bin/sh
set -e

echo "📡 Esperando a la base de datos..."
while ! nc -z "$DB_HOST" 5432; do
  sleep 1
done
echo "✅ Base de datos lista."

echo "🔍 Esperando a que exista la tabla django_migrations..."

until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT to_regclass('public.django_migrations');" 2>/dev/null | grep -q django_migrations; do
  echo "⏳ La tabla django_migrations aún no existe. Esperando..."
  sleep 2
done

echo "✅ Tabla django_migrations encontrada."

echo "🔍 Esperando a que se apliquen las migraciones de django_celery_beat..."

until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT 1 FROM django_migrations WHERE app='django_celery_beat' AND name='0001_initial';" \
  | grep -q 1; do
  echo "⏳ Migraciones de django_celery_beat aún no aplicadas. Esperando..."
  sleep 2
done

echo "✅ Migraciones de django_celery_beat detectadas."

exec "$@"

