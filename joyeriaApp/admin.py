from django.contrib import admin

# Register your models here.

from .models import Marca, Articulo

admin.site.register(Marca)
admin.site.register(Articulo)