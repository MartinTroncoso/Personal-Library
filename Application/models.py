from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    telefono = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        db_table = "Usuario"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username


class Libro(models.Model):
    ESTADO_CHOICES = [
        ("LEIDO", "Leído"),
        ("NO_LEIDO", "No leído"),
        ("EN_PROGRESO", "En progreso"),
    ]

    usuario = models.ManyToManyField(Usuario, related_name="libros")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="NO_LEIDO")
    titulo = models.CharField(max_length=150)
    subtitulo = models.CharField(max_length=150, null=True, blank=True)
    descripcion = models.TextField()
    autores = models.CharField(max_length=500)
    fecha = models.DateField(null=True, blank=True)
    portada = models.URLField(max_length=200, null=True, blank=True)
    visibilidad = models.CharField(max_length=10, default="UNKNOWN")
    link_lectura = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "Libro"
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

    def __str__(self):
        return self.titulo


class LibroDelDia(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=150, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    autores = models.CharField(max_length=500, null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    portada = models.URLField(max_length=200, null=True, blank=True)
    visibilidad = models.CharField(max_length=10, default="UNKNOWN")
    link_lectura = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "LibroDelDia"
        verbose_name = "LibroDelDia"

    def __str__(self):
        return self.titulo
