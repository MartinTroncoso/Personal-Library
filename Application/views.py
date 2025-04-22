from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
                    user = models.Usuario.objects.create(username=username, password=password, email=email)
                    user.save()
                    return redirect('index')
                except IntegrityError:
                    form_register.add_error('username', 'El usuario ingresado ya está registrado')
                    return render(request, "register.html", {"form_register": form_register, 'timestamp' : now().timestamp()})
            else:
                form_register.add_error('password2', 'Las contraseñas no coinciden')
                return render(request, "register.html", {"form_register": form_register, 'timestamp' : now().timestamp()})
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
    if request.method == 'POST':
        form_add_libro = forms.Add_Libro(request.POST)
        
        if form_add_libro.is_valid():
            titulo = form_add_libro.cleaned_data['titulo']
            descripcion = form_add_libro.cleaned_data['descripcion']
            autor = form_add_libro.cleaned_data['autor']
            fecha = form_add_libro.cleaned_data['fecha']
            leido = form_add_libro.cleaned_data['leido']
            
            libro = models.Libro(titulo=titulo, descripcion=descripcion, autor=autor, fecha=fecha, leido=leido, usuario=request.user)
            libro.save()
            
            return redirect('biblioteca')
        else:
            form_add_libro.add_error(None, 'Error al agregar el libro')
            return render(request, "add_libro.html", {"form_add_libro": form_add_libro, 'timestamp' : now().timestamp()})
    else:
        form_add_libro = forms.Add_Libro()
        
    return render(request, "add_libro.html", {"form_add_libro": form_add_libro, 'timestamp' : now().timestamp()})