import redis  # type: ignore

from django.conf import settings
from django.db import connection
from django.http import HttpRequest, JsonResponse


def health_check(request: HttpRequest) -> JsonResponse:
    checks = {
        "status": "ok",
        "database": "ok",
        "redis": "ok",
        "version": settings.APP_VERSION,
    }

    # DB check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        checks["database"] = "error"
        checks["status"] = "error"

    # Redis check
    try:
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
    except Exception:
        checks["redis"] = "error"
        checks["status"] = "error"

    status_code = 200 if checks["status"] == "ok" else 503
    return JsonResponse(checks, status=status_code)
