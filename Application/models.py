from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=15, null=True, blank=True)
    
    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return self.username
    
class Libro(models.Model):
    usuario = models.ManyToManyField(Usuario, related_name='libros')
    leido = models.BooleanField(default=False)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    autores = models.CharField(max_length=50)
    fecha = models.DateField(null=True, blank=True)
    portada = models.URLField(max_length=200, null=True, blank=True)
    
    class Meta:
        db_table = 'Libro'
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        
    def __str__(self):
        return self.titulo