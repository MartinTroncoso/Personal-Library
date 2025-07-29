FROM python:3.11-slim

RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Copiar el script de entrada
COPY docker/entrypoint.sh /entrypoint.sh
COPY docker/entrypoint-celery.sh /entrypoint-celery.sh
RUN chmod +x /entrypoint.sh /entrypoint-celery.sh

# Usar como entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Comando por defecto (se pasa a "$@" en el entrypoint)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
