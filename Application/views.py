import json
from datetime import datetime
from typing import Union

from dateutil import parser  # type: ignore
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
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


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form_login = forms.Login(request.POST)

        if form_login.is_valid():
            username = form_login.cleaned_data["username"]
            password = form_login.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                form_login.add_error(None, "Usuario o contraseña incorrectos")
                return render(
                    request,
                    "login.html",
                    {"form_login": form_login, "timestamp": now().timestamp()},
                )
    else:
        form_login = forms.Login()

    # A dictionary which keys are str and the values can be either forms.Login or float
    context: dict[str, Union[forms.Login, float]] = {
        "form_login": form_login,
        "timestamp": now().timestamp(),
    }

    return render(request, "login.html", context)


def register_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
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
                    return redirect("index")
                except IntegrityError:
                    form_register.add_error(
                        None, "El usuario ingresado ya está registrado"
                    )
            else:
                form_register.add_error(None, "Las contraseñas no coinciden")
    else:
        form_register = forms.Register()

    return render(
        request,
        "register.html",
        {"form_register": form_register, "timestamp": now().timestamp()},
    )


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("login")


# ----------- VISTAS ----------- #


@login_required
def index(request: HttpRequest) -> HttpResponse:
    libro_del_dia = models.LibroDelDia.objects.last()

    if fecha_ultimo_libro_agregado:
        datos_fecha = {
            "year": fecha_ultimo_libro_agregado.year,
            "month": meses[fecha_ultimo_libro_agregado.month - 1],
            "day": fecha_ultimo_libro_agregado.day,
            "hour": fecha_ultimo_libro_agregado.strftime("%H:%M:%S"),
        }
    else:
        datos_fecha: dict = {}

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
    libros = models.Libro.objects.filter(usuario=request.user.id)
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

            if not models.Libro.objects.filter(
                titulo=nuevo_libro.titulo,
                subtitulo=nuevo_libro.subtitulo,
                autores=nuevo_libro.autores,
            ).exists():
                nuevo_libro.save()
                nuevo_libro.usuario.set([request.user.id])
                global fecha_ultimo_libro_agregado
                fecha_ultimo_libro_agregado = datetime.now()
                return JsonResponse({"status": "success", "accion": "nuevo"})
            elif request.user.id not in models.Libro.objects.get(
                titulo=nuevo_libro.titulo,
                subtitulo=nuevo_libro.subtitulo,
                autores=nuevo_libro.autores,
            ).usuario.values_list("id", flat=True):
                models.Libro.objects.get(
                    titulo=nuevo_libro.titulo, autores=nuevo_libro.autores
                ).usuario.add(request.user.id)
                fecha_ultimo_libro_agregado = datetime.now()
                return JsonResponse(
                    {"status": "success", "accion": "existente_nuevo_usuario"}
                )
            else:
                return JsonResponse({"status": "success", "accion": "repetido"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return render(request, "add_libro.html", {"timestamp": now().timestamp()})


@login_required
def libro_view(request: HttpRequest, id: int) -> HttpResponse:
    libro = get_object_or_404(models.Libro, id=id)

    if request.method == "POST":
        try:
            estado = request.POST.get("estado")
            models.Libro.objects.filter(id=id).update(estado=estado)
            return redirect("biblioteca")
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return render(
        request, "libro.html", {"libro": libro, "timestamp": now().timestamp()}
    )


@login_required
def libro_del_dia_view(request: HttpRequest) -> HttpResponse:
    libro_del_dia = models.LibroDelDia.objects.last()

    if request.method == "POST":
        try:
            if not models.Libro.objects.filter(
                titulo=libro_del_dia.titulo,
                subtitulo=libro_del_dia.subtitulo,
                autores=libro_del_dia.autores,
            ).exists():
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

                return JsonResponse(
                    {
                        "status": "success",
                        "accion": "nuevo",
                        "message": "Libro del día agregado a tu biblioteca",
                    }
                )
            elif request.user.id not in models.Libro.objects.get(
                titulo=libro_del_dia.titulo,
                subtitulo=libro_del_dia.subtitulo,
                autores=libro_del_dia.autores,
            ).usuario.values_list("id", flat=True):
                models.Libro.objects.get(
                    titulo=libro_del_dia.titulo, autores=libro_del_dia.autores
                ).usuario.add(request.user.id)
                fecha_ultimo_libro_agregado = datetime.now()
                return JsonResponse(
                    {
                        "status": "success",
                        "accion": "existente_nuevo_usuario",
                        "message": "Libro del día agregado a tu biblioteca",
                    }
                )
            else:
                return JsonResponse(
                    {
                        "status": "success",
                        "accion": "repetido",
                        "message": "El libro del día ya está en tu biblioteca",
                    }
                )
        except Exception:
            messages.error(request, "Error al agregar el libro del día a tu biblioteca")
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
        messages.success(request, "Libro eliminado correctamente")
        return redirect("biblioteca")
    except Exception:
        messages.error(request, "Error al eliminar el libro")
        return redirect("biblioteca")


def cantidad_libros_guardados(user_id: int) -> int:
    return models.Libro.objects.filter(usuario=user_id).count()
