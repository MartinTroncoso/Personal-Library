import logging
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger("Application")


class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception:
            logger.error("Unhandled exception", exc_info=True)

            # If it is API (accepts JSON), we reply JSON
            if request.headers.get("Accept") == "application/json":
                return JsonResponse({"error": "Internal server error"}, status=500)

            # If it is normal request, we reply template 500
            return render(request, "500.html", status=500)


# With special method __call__ we can define an object and execute it as a function
# globalExc = GlobalExceptionMiddleware()
# globalExc()
