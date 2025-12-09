#!/bin/sh
set -e

echo "📡 Waiting for PostgreSQL to be ready..."

until pg_isready -h "$DB_HOST" -p 5432 -U "$DB_USER"; do
  echo "🔄 Waiting for pg_isready response..."
  sleep 1
done

until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; do
  echo "⏳ Waiting for data base to be completely operational..."
  sleep 1
done

echo "✅ Data base ready."

echo "⚙️ Applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "🛠️ Configuring periodic tasks..."
python manage.py setup_periodic_tasks

echo "📚 Selecting book of the day..."
python manage.py shell -c "from Application.tasks import libro_del_dia; libro_del_dia()"

echo "🚀 Initiating server with command: $@"
exec "$@"
