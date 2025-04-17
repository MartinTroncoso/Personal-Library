from django.db import models

class Libro(models.Model):
    leido = models.BooleanField(default=False)

class Usuario(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)