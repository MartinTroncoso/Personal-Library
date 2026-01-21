from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest


class AuthService:
    @staticmethod
    def login_user(request: HttpRequest, username: str, password: str) -> bool:
        user = authenticate(username=username, password=password)

        if not user:
            return False

        login(request, user)
        return True

    @staticmethod
    def logout_user(request: HttpRequest) -> None:
        logout(request)
