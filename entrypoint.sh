#!/bin/sh
set -e

echo "📡 Esperando a que PostgreSQL esté listo..."

until pg_isready -h "$DB_HOST" -p 5432 -U "$DB_USER"; do
  echo "🔄 Esperando respuesta de pg_isready..."
  sleep 1
done

until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; do
  echo "⏳ Esperando a que la base de datos esté completamente operativa..."
  sleep 1
done

echo "✅ Base de datos lista."

echo "⚙️ Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate

echo "🛠️ Configurando tareas periódicas..."
python manage.py setup_periodic_tasks

echo "🚀 Iniciando servidor con comando: $@"
exec "$@"