from django.shortcuts import render
from .forms import ArticuloForm,MarcaForm
from django.http import HttpResponse
from .models import Marca,Articulo
from django.template import loader

# Create your views here.

def index(request):
    return render(request, 'index.html')

def gallery(request):
    return render(request, 'gallery.html')

def services(request):
    return render(request, '404.html')

def news(request):
    return render(request, 'news.html')

def mail(request):
    return render(request, 'mail.html')

def single(request):
    return render(request, 'single.html')

def crear_articulo(request):
    if request.method == 'POST':
        articulo_form = ArticuloForm(request.POST, request.FILES)
        marca_form = MarcaForm(request.POST)
        if articulo_form.is_valid() & marca_form.is_valid():
            art = articulo_form.save(commit=False)
            marca = marca_form.save()
            art.articulo_marca = marca
            art.save()
            return HttpResponse('Guardado correctamente')