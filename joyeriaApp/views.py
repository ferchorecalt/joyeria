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

def crear_marca(request):
    if request.method == 'POST':
        marca_form = MarcaForm(request.POST)
        if marca_form.is_valid():
            marca = marca_form.save()
            # return HttpResponse('Guardado correctamente')
            marca_form=MarcaForm()
            return render(request, 'crearMarca.html', {'form': marca_form,'resultado':'Marca guardada con exito!','verForm':False})
        else:  return render(request, 'crearMarca.html', {'form': marca_form,'resultado':'La marca no pudo registrarse','verForm':False})
    else:
        marca_form = MarcaForm()

    return render(request, 'crearMarca.html', {'form': marca_form,'verForm':True})

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
    else:
        articulo_form = ArticuloForm()

    return render(request, 'crearArticulo.html', {'form': articulo_form})