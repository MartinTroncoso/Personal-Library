FROM python:3.11-slim

# Avoids .pyc files and yields direct logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ ./requirements/

# Install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements/dev.txt

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
