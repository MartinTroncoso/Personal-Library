import json

from django.contrib.auth import logout
from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

from authentication.services import AuthService


# @csrf_exempt  # We use it here because login with JSON does not modify sensible data
@ensure_csrf_cookie
def login_view(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        # Set CSRF token
        return JsonResponse({"detail": "CSRF cookie set"})

    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False}, status=400)

    success = AuthService.login_user(
        request,
        data.get("username"),
        data.get("password"),
    )

    if not success:
        return JsonResponse({"success": False}, status=401)

    return JsonResponse({"success": True})


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
