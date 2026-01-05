import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods


# @csrf_exempt  # We use it here because login with JSON does not modify sensible data
@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        return JsonResponse({"detail": "CSRF cookie set"})

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return JsonResponse(
            {"error": "Username and password required"},
            status=400,
        )

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    login(request, user)

    return JsonResponse({"success": True, "message": "Login successful"})


def logout_json(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    if not request.user.is_authenticated:
        # It allows idempotent logout: logging out 2 times does not give any error
        return JsonResponse({"status": "already_logged_out"})

    logout(request)

    return JsonResponse({"success": True, "status": "logged_out"})


def test_url(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        return JsonResponse({"test": "swccess"})
    else:
        return JsonResponse({"test": "failure"})


def csrf_token(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"csrftoken": get_token(request)})
