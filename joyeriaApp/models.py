from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Marca(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    imagen = models.ImageField(upload_to='%Y/%m/%d')
    descripcion = models.CharField(max_length=500) #De ultima, si no tienen, la deja en blanco
    def __str__(self):
        return '%s' % (self.nombre)
    def what_i_need_in_ajax_call_for_marca(self):  #METODO QUE ES UTILIZADO EN VIEWS.PY PARA DEVOLVER LO QUE YO QUIERA DEL OBJETO EN UN LLAMADO AJAX
        return {
            "nombre": self.nombre,
            "imagen" : self.imagen.url,
            "descripcion": self.descripcion,
            "pk": self.id,
            "articulos": list(map(lambda x: x.what_i_need_in_ajax_call_for_articulo_from_marca(),  self.articulo_set.all()))
        }

class Articulo(models.Model):
    modelo = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=500)
    fecha = models.DateTimeField(auto_now_add =True)
    imagen = models.ImageField(upload_to='%Y/%m/%d')
    articulo_marca=models.ForeignKey(Marca, on_delete=models.CASCADE)
    def what_i_need_in_ajax_call_for_articulo(self): #METODO QUE ES UTILIZADO EN VIEWS.PY PARA DEVOLVER LO QUE YO QUIERA DEL OBJETO EN UN LLAMADO AJAX
        return {
            "modelo": self.modelo,
            "descripcion": self.descripcion,
            "fecha" : self.fecha.isoformat(),
            "imagen" : self.imagen.url,
            "nombre_marca": self.articulo_marca.nombre,
            "id_marca" : self.articulo_marca.id,
            "pk": self.id
        }
    def what_i_need_in_ajax_call_for_articulo_from_marca(self): #METODO QUE ES UTILIZADO EN VIEWS.PY PARA DEVOLVER LO QUE YO QUIERA DEL OBJETO EN UN LLAMADO AJAX
        return {
            "modelo": self.modelo,
            "imagen" : self.imagen.url,
            "pk": self.id
        }
