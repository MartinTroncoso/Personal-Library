import json

from django.contrib.auth import authenticate, login
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login_view(request: HttpRequest) -> JsonResponse:
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

    return JsonResponse({"message": "Login successful"})
