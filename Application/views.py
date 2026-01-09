import json
import logging
from datetime import datetime
from typing import Union
from .helpers import (
    book_has_been_saved_by_someone,
    book_has_not_been_saved_by_current_user,
)
from dateutil import parser  # type: ignore
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.middleware.csrf import get_token
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.views.decorators.http import require_POST

import Application.forms as forms
import Application.models as models

fecha_ultimo_libro_agregado = None
meses = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]

logger = logging.getLogger(__name__)


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        logger.info("User is already authenticated, redirecting to home page")
        return redirect("index")

    if request.method == "POST":
        form_login = forms.Login(request.POST)

        if form_login.is_valid():
            username = form_login.cleaned_data["username"]
            password = form_login.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                logger.info("Login successful!")
                return redirect("index")
            else:
                form_login.add_error(None, "Incorrect user or password")
                logger.error("Incorrect user or password.")
                return render(
                    request,
                    "login.html",
                    {"form_login": form_login, "timestamp": now().timestamp()},
                )
    else:
        form_login = forms.Login()

    # A dictionary which keys are strings and the values can be either forms.Login or float
    context: dict[str, Union[forms.Login, float]] = {
        "form_login": form_login,
        "timestamp": now().timestamp(),
    }

    return render(request, "login.html", context)


def register_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        logger.info("User is already authenticated, redirecting to home page")
        return redirect("index")

    if request.method == "POST":
        form_register = forms.Register(request.POST)

        if form_register.is_valid():
            username = form_register.cleaned_data["username"]
            password = form_register.cleaned_data["password"]
            password2 = form_register.cleaned_data["password2"]
            email = form_register.cleaned_data["email"]

            if password == password2:
                try:
                    Usuario = get_user_model()
                    usuario = Usuario.objects.create_user(
                        username=username, password=password, email=email
                    )
                    login(request, usuario)
                    logger.info("User registered successfully!")
                    return redirect("index")
                except IntegrityError:
                    form_register.add_error(None, "The user is already registered")
                    logger.error("The user is already registered.")
            else:
                form_register.add_error(None, "The passwords do not match")
                logger.error("The passwords do not match.")
    else:
        form_register = forms.Register()

    return render(
        request,
        "register.html",
        {"form_register": form_register, "timestamp": now().timestamp()},
    )


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    logger.info("Logging out...")
    return redirect("login")


# ----------- VISTAS ----------- #


@login_required
def index(request: HttpRequest) -> HttpResponse:
    libro_del_dia = models.LibroDelDia.objects.last()
    datos_fecha: dict = {}

    if fecha_ultimo_libro_agregado:
        datos_fecha = {
            "year": fecha_ultimo_libro_agregado.year,
            "month": meses[fecha_ultimo_libro_agregado.month - 1],
            "day": fecha_ultimo_libro_agregado.day,
            "hour": fecha_ultimo_libro_agregado.strftime("%H:%M:%S"),
        }

    return render(
        request,
        "index.html",
        {
            "libro_del_dia": libro_del_dia,
            "cantidad_libros_guardados": cantidad_libros_guardados(request.user.id),
            "fecha_ultimo_libro_agregado": fecha_ultimo_libro_agregado,
            "datos_fecha": datos_fecha,
            "timestamp": now().timestamp(),
            "ultimo_libro_agregado": models.Libro.objects.last(),
        },
    )


@login_required
def biblioteca_view(request: HttpRequest) -> HttpResponse:
    libros = models.Libro.objects.prefetch_related("usuario").filter(
        usuario=request.user
    )
    return render(
        request, "biblioteca.html", {"libros": libros, "timestamp": now().timestamp()}
    )


@login_required
def add_libro_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        try:
            datos = json.loads(request.body)

            fecha_parseada = parser.parse(datos["fecha_publicacion"])

            nuevo_libro = models.Libro(
                titulo=datos["titulo"],
                subtitulo=datos["subtitulo"],
                descripcion=datos["descripcion"],
                autores=datos["autores"],
                fecha=fecha_parseada,
                portada=datos["portada"],
                visibilidad=datos["visibilidad"],
                link_lectura=datos["link_lectura"],
            )

            if not book_has_been_saved_by_someone(nuevo_libro):
                nuevo_libro.save()
                nuevo_libro.usuario.set([request.user.id])
                global fecha_ultimo_libro_agregado
                fecha_ultimo_libro_agregado = datetime.now()

                logger.info("New book added")

                return JsonResponse({"status": "success", "accion": "nuevo"})
            elif book_has_not_been_saved_by_current_user(request.user.id, nuevo_libro):
                models.Libro.objects.get(
                    titulo=nuevo_libro.titulo, autores=nuevo_libro.autores
                ).usuario.add(request.user.id)
                fecha_ultimo_libro_agregado = datetime.now()

                logger.info("A new user added the book")

                return JsonResponse(
                    {"status": "success", "accion": "existente_nuevo_usuario"}
                )
            else:
                logger.debug("The book is already in your library")
                return JsonResponse({"status": "success", "accion": "repetido"})
        except Exception as e:
            logger.error(str(e))
            return JsonResponse({"status": "error", "message": str(e)})

    return render(request, "add_libro.html", {"timestamp": now().timestamp()})


@login_required
def libro_view(request: HttpRequest, id: int) -> HttpResponse:
    libro = get_object_or_404(models.Libro, id=id)

    if request.method == "POST":
        try:
            estado = request.POST.get("estado")
            models.Libro.objects.filter(id=id).update(estado=estado)
            logger.info(f"Book state changed to {estado}")
            return redirect("biblioteca")
        except Exception as e:
            logger.error(str(e))
            return JsonResponse({"status": "error", "message": str(e)})

    return render(
        request, "libro.html", {"libro": libro, "timestamp": now().timestamp()}
    )


@login_required
def libro_del_dia_view(request: HttpRequest) -> HttpResponse:
    libro_del_dia = models.LibroDelDia.objects.last()

    if request.method == "POST":
        try:
            if not book_has_been_saved_by_someone(libro_del_dia):
                models.Libro.objects.create(
                    titulo=libro_del_dia.titulo,
                    subtitulo=libro_del_dia.subtitulo,
                    descripcion=libro_del_dia.descripcion,
                    autores=libro_del_dia.autores,
                    fecha=libro_del_dia.fecha,
                    portada=libro_del_dia.portada,
                    visibilidad=libro_del_dia.visibilidad,
                    link_lectura=libro_del_dia.link_lectura,
                ).usuario.set([request.user.id])

                global fecha_ultimo_libro_agregado
                fecha_ultimo_libro_agregado = datetime.now()

                logger.info("Book of the day added to your library.")

                return JsonResponse(
                    {
                        "status": "success",
                        "accion": "nuevo",
                        "message": "Book of the day added to your library",
                    }
                )
            elif book_has_not_been_saved_by_current_user(
                request.user.id, libro_del_dia
            ):
                models.Libro.objects.get(
                    titulo=libro_del_dia.titulo, autores=libro_del_dia.autores
                ).usuario.add(request.user.id)
                fecha_ultimo_libro_agregado = datetime.now()

                logger.info("Book of the day added to your library.")

                return JsonResponse(
                    {
                        "status": "success",
                        "accion": "existente_nuevo_usuario",
                        "message": "Book of the day added to your library",
                    }
                )
            else:
                logger.info("The book of the day is already in your library.")
                return JsonResponse(
                    {
                        "status": "success",
                        "accion": "repetido",
                        "message": "The book of the day is already in your library",
                    }
                )
        except Exception as e:
            # Visible to the user in the UI, not shown in console or logs
            messages.error(
                request, "Error upon adding the book of the day to your library"
            )

            # Shown in the console and logs
            logger.error(str(e))
            return redirect("index")

    return render(
        request,
        "libro_del_dia.html",
        {"libro_del_dia": libro_del_dia, "timestamp": now().timestamp()},
    )


@login_required
@require_POST
def delete_libro_view(request: HttpRequest, id: int) -> HttpResponse:
    try:
        libro = get_object_or_404(models.Libro, id=id)
        libro.delete()
        messages.success(request, "Book deleted successfully")
        logger.info("Book deleted successfully.")
        return redirect("biblioteca")
    except Exception as e:
        messages.error(request, "Error upon deleting the book")
        logger.error(str(e))
        return redirect("biblioteca")


def cantidad_libros_guardados(user_id: int) -> int:
    return (
        models.Libro.objects.prefetch_related("usuario").filter(usuario=user_id).count()
    )


def csrf(request: HttpRequest) -> HttpResponse:
    return JsonResponse({"csrftoken": get_token(request)})


def test_error(request: HttpRequest) -> BaseException:
    raise ValueError("Test error")
