from django import forms

class Login(forms.Form):
    username = forms.CharField(label='Nombre de usuario', widget=forms.TextInput(attrs={'class': 'form-label form-control mb-3'}), max_length=50)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-label form-control mb-3'}), max_length=50)
    
class Register(forms.Form):
    username = forms.CharField(label = 'Nombre de usuario', widget=forms.TextInput(attrs={'class': 'form-label form-control mb-3'}), max_length=50)
    password = forms.CharField(label = 'Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-label form-control mb-3'}), max_length=50)
    password2 = forms.CharField(label = 'Repetir contraseña', widget=forms.PasswordInput(attrs={'class': 'form-label form-control mb-3'}), max_length=50)
    email = forms.EmailField(label = 'Email', widget=forms.EmailInput(attrs={'class': 'form-label form-control mb-3'}), max_length=50)