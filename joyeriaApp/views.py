from django.shortcuts import render
from .forms import ArticuloForm,MarcaForm
from django.http import HttpResponse
from .models import Marca,Articulo

# Create your views here.

def crear_articulo(request):
    if request.method == 'POST':
        articulo_form = ArticuloForm(request.POST, request.FILES)
        marca_form = MarcaForm(request.POST)
        if articulo_form.is_valid() & marca_form.is_valid():
            art = articulo_form.save()
            marca = marca_form.save()
            art.articulo_marca = marca
            return HttpResponse('Guardado correctamente')