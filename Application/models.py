from django.db import models

class Usuario(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    
    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return self.username
    
class Libro(models.Model):
    usuario = models.ManyToManyField(Usuario, related_name='libros')
    leido = models.BooleanField(default=False)
    titulo = models.CharField(max_length=50)
    descripción = models.TextField()
    autor = models.CharField(max_length=50)
    fecha = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'Libro'
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        
    def __str__(self):
        return self.titulo