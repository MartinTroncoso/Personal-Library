from django.contrib.auth.models import AbstractUser
from django.db import models

from typing import Any


class Usuario(AbstractUser):
    telefono: Any = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        db_table = "Usuario"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self) -> str:
        return self.username


class Libro(models.Model):
    ESTADO_CHOICES = [
        ("LEIDO", "Leído"),
        ("NO_LEIDO", "No leído"),
        ("EN_PROGRESO", "En progreso"),
    ]

    usuario: Any = models.ManyToManyField(Usuario, related_name="libros")
    estado: Any = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default="NO_LEIDO"
    )
    titulo: Any = models.CharField(max_length=150)
    subtitulo: Any = models.CharField(max_length=150, null=True, blank=True)
    descripcion: Any = models.TextField()
    autores: Any = models.CharField(max_length=500)
    fecha: Any = models.DateField(null=True, blank=True)
    portada: Any = models.URLField(max_length=200, null=True, blank=True)
    visibilidad: Any = models.CharField(max_length=10, default="UNKNOWN")
    link_lectura: Any = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "Libro"
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

    def __str__(self) -> str:
        return self.titulo


class LibroDelDia(models.Model):
    titulo: Any = models.CharField(max_length=200)
    subtitulo: Any = models.CharField(max_length=150, null=True, blank=True)
    descripcion: Any = models.TextField(null=True, blank=True)
    autores: Any = models.CharField(max_length=500, null=True, blank=True)
    fecha: Any = models.DateField(null=True, blank=True)
    portada: Any = models.URLField(max_length=200, null=True, blank=True)
    visibilidad: Any = models.CharField(max_length=10, default="UNKNOWN")
    link_lectura: Any = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "LibroDelDia"
        verbose_name = "LibroDelDia"

    def __str__(self) -> str:
        return self.titulo
