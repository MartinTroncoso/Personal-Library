import json
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from dateutil import parser # type: ignore

import Application.forms as forms
import Application.models as models

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form_login = forms.Login(request.POST)
        
        if form_login.is_valid():
            username = form_login.cleaned_data['username']
            password = form_login.cleaned_data['password']
            
            user = authenticate(request, username = username, password = password)
            
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form_login.add_error(None, 'Usuario o contraseña incorrectos')
                return render(request, "login.html", {"form_login": form_login, 'timestamp' : now().timestamp()})
    else:
        form_login = forms.Login()
        
    return render(request, "login.html", {"form_login": form_login, 'timestamp' : now().timestamp()})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form_register = forms.Register(request.POST)
        
        if form_register.is_valid():
            username = form_register.cleaned_data['username']
            password = form_register.cleaned_data['password']
            password2 = form_register.cleaned_data['password2']
            email = form_register.cleaned_data['email']
            
            if password == password2:
                try:
                    Usuario = get_user_model()
                    usuario = Usuario.objects.create_user(username=username, password=password, email=email)
                    login(request, usuario)
                    return redirect('index')
                except IntegrityError:
                    form_register.add_error(None, 'El usuario ingresado ya está registrado')
            else:
                form_register.add_error(None, 'Las contraseñas no coinciden')
    else:
        form_register = forms.Register()
            
    return render(request, "register.html", {"form_register": form_register, 'timestamp' : now().timestamp()})
            
        
def logout_view(request):
    logout(request)
    return redirect('login')

################ VISTAS ################

@login_required
def index(request):
    return render(request, 'index.html', {'timestamp' : now().timestamp()})

@login_required
def biblioteca_view(request):
    libros = models.Libro.objects.filter(usuario=request.user.id)
    return render(request, "biblioteca.html", {"libros": libros, 'timestamp' : now().timestamp()})

@login_required
def add_libro_view(request):
    import logging
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            
            fecha_parseada = parser.parse(datos['fecha_publicacion'])
            
            nuevo_libro = models.Libro(titulo=datos['titulo'], descripcion=datos['descripcion'], autores=datos['autores'], fecha=fecha_parseada, portada=datos['portada'])

            if not models.Libro.objects.filter(titulo = nuevo_libro.titulo, autores = nuevo_libro.autores).exists():
                nuevo_libro.save()
                nuevo_libro.usuario.set([request.user.id])
                logger.info(f"NUEVO LIBRO PAPITO {nuevo_libro} de {nuevo_libro.autores}")
                return JsonResponse({'status': 'success', 'accion' : 'nuevo'})
            elif request.user.id not in models.Libro.objects.get(titulo = nuevo_libro.titulo, autores = nuevo_libro.autores).usuario.values_list('id', flat=True):
                models.Libro.objects.get(titulo = nuevo_libro.titulo, autores = nuevo_libro.autores).usuario.add(request.user.id)
                logger.info(f"EL LIBRO YA EXISTÍA Y TIENE UN NUEVO USUARIO {request.user.username}")
                return JsonResponse({'status': 'success', 'accion' : 'existente_nuevo_usuario'})
            else:
                logger.info(f"EL USUARIO {request.user.username} YA TIENE ESTE LIBRO")
                return JsonResponse({'status': 'success', 'accion' : 'repetido'})
        except Exception as e:
            logger.exception("Error al guardar libro")
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return render(request, "add_libro.html", {'timestamp' : now().timestamp()})

@login_required
def libro_view(request, id):
    libro = get_object_or_404(models.Libro, id=id)
    return render(request, "libro.html", {"libro": libro, 'timestamp' : now().timestamp()})
        
# @login_required
# def add_libro_view(request):
#     if request.method == 'POST':
#         form_add_libro = forms.Add_Libro(request.POST)
        
#         if form_add_libro.is_valid():
#             titulo = form_add_libro.cleaned_data['titulo']
#             descripcion = form_add_libro.cleaned_data['descripcion']
#             autor = form_add_libro.cleaned_data['autor']
#             fecha = form_add_libro.cleaned_data['fecha']
#             leido = form_add_libro.cleaned_data['leido']
            
#             libro = models.Libro(titulo=titulo, descripcion=descripcion, autor=autor, fecha=fecha, leido=leido, usuario=request.user)
#             libro.save()
            
#             return redirect('biblioteca')
#         else:
#             form_add_libro.add_error(None, 'Error al agregar el libro')
#             return render(request, "add_libro.html", {"form_add_libro": form_add_libro, 'timestamp' : now().timestamp()})
#     else:
#         form_add_libro = forms.Add_Libro()
        
#     return render(request, "add_libro.html", {"form_add_libro": form_add_libro, 'timestamp' : now().timestamp()})

@login_required
@require_POST
def delete_libro_view(request,id):
    try:
        libro = get_object_or_404(models.Libro, id=id)
        libro.delete()
        messages.success(request, 'Libro eliminado correctamente')
        return redirect('biblioteca')
    except Exception as e:
        messages.error(request, 'Error al eliminar el libro')
        return redirect('biblioteca')