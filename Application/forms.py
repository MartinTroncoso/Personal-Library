from django import forms


class Login(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={"class": "form-label form-control mb-3"}),
        max_length=50,
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-label form-control mb-3"}),
        max_length=50,
    )


class Register(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={"class": "form-label form-control mb-3"}),
        max_length=50,
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-label form-control mb-3"}),
        max_length=50,
    )
    password2 = forms.CharField(
        label="Repetir contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-label form-control mb-3"}),
        max_length=50,
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-label form-control mb-3"}),
        max_length=50,
    )


class Add_Libro(forms.Form):
    titulo = forms.CharField(
        label="Título",
        widget=forms.TextInput(attrs={"class": "form-label form-control mb-3"}),
        max_length=50,
    )
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={"class": "form-label form-control mb-3"}),
        max_length=500,
    )
    autor = forms.CharField(
        label="Autor",
        widget=forms.TextInput(attrs={"class": "form-label form-control mb-3"}),
        max_length=50,
    )
    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(
            attrs={"class": "form-label form-control mb-3", "type": "date"}
        ),
        required=False,
    )
    leido = forms.BooleanField(
        label="Leído",
        widget=forms.CheckboxInput(attrs={"class": "form-label form-check-input mb-3"}),
        required=False,
    )
