from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.contrib.auth import authenticate, login

from Application.forms import Login, Register 

import Application.models as models

def index(request):
    return render(request, 'index.html', {'timestamp' : now().timestamp()})

def login_view(request):
    if request.method == 'POST':
        form_login = Login(request.POST)
        
        if form_login.is_valid():
            username = form_login.cleaned_data['username']
            password = form_login.cleaned_data['password']
            
            user = authenticate(request, username = username, password = password)
            
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form_login.add_error(None, 'Invalid username or password')
                return render(request, "login.html", {"form_login": form_login, 'timestamp' : now().timestamp()})
    else:
        form_login = Login()
        
    return render(request, "login.html", {"form_login": form_login, 'timestamp' : now().timestamp()})

def register_view(request):
    if request.method == 'POST':
        form_register = Register(request.POST)
        
        if form_register.is_valid():
            username = form_register.cleaned_data['username']
            password = form_register.cleaned_data['password']
            password2 = form_register.cleaned_data['password2']
            email = form_register.cleaned_data['email']
            
            if password == password2:
                try:
                    user = models.Usuario.objects.create(username=username, password=password, email=email)
                    user.save()
                    return redirect('/')
                except IntegrityError:
                    form_register.add_error('username', 'El usuario ingresado ya está registrado')
                    return render(request, "register.html", {"form_register": form_register, 'timestamp' : now().timestamp()})
            else:
                form_register.add_error('password2', 'Las contraseñas no coinciden')
                return render(request, "register.html", {"form_register": form_register, 'timestamp' : now().timestamp()})
    else:
        form_register = Register()
            
    return render(request, "register.html", {"form_register": form_register, 'timestamp' : now().timestamp()})
            
        
def logout(request):
    logout(request)
    return redirect('/')