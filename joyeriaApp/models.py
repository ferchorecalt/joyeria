from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Marca(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    imagen = models.ImageField(upload_to='%Y/%m/%d')
    descripcion = models.CharField(max_length=500) #De ultima, si no tienen, la deja en blanco
    def __str__(self):
        return '%s' % (self.nombre)

class Articulo(models.Model):
    modelo = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=500)
    fecha = models.DateTimeField(auto_now_add =True)
    imagen = models.ImageField(upload_to='%Y/%m/%d')
    articulo_marca=models.ForeignKey(Marca, on_delete=models.CASCADE)