from django.shortcuts import render,render_to_response,redirect
from .forms import ArticuloForm,MarcaForm,UserForm,ContactForm
from django.http import *
from .models import Marca,Articulo
from django.template import loader,RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
import json
import sys
from django.core import serializers
from django.template.loader import render_to_string,get_template

# Create your views here.

def index(request):
    # context = RequestContext(request)
    # context['text'] = _("Welcome to Pythonizame");
    return render(request, 'index.html')

def gallery(request):
    return render(request, 'gallery.html')

def services(request):
    return render(request, '404.html')

def news(request):
    return render(request, 'news.html')

def mail(request):
    # return render(request, 'mail.html')
    form_class = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            mail = form.cleaned_data['mail']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']
            send_mail(asunto, mensaje, mail, ['ferchorecalt@gmail.com'])
            return redirect('mail')
    return render(request, 'mail.html', {
        'form': form_class,
    })

def single(request, pk):
    articulo = Articulo.objects.get(pk=pk)
    return render(request, 'single.html', {'articulo':articulo})

def singleMarca(request, pk):
    marca = Marca.objects.get(pk=pk)
    return render(request, 'singleMarca.html', {'marca':marca})

@login_required(login_url='login.html')
def editarArticulo(request, pk):
    if request.method == 'GET':
        articulo = Articulo.objects.get(pk=pk)
        articulo_form = ArticuloForm(instance=articulo)
        return render(request, 'editarArticulo.html', {'form': articulo_form,'id':articulo.pk})
    else:
        articulo_editar = Articulo.objects.get(pk=pk)
        articulo_form = ArticuloForm(request.POST, request.FILES,instance=articulo_editar)
        if articulo_form.is_valid():
            articulo_form.save()
            # return HttpResponse('Guardado correctamente')
            return redirect('listadoArticulos')

def eliminarArticulo(request, pk):
    articulo = Articulo.objects.get(pk=pk)
    articulo.delete()
    return redirect('listadoArticulos')

def eliminarMarca(request, pk):
    marca = Marca.objects.get(pk=pk)
    marca.delete()
    return redirect('listadoMarcas')

def editarMarca(request, pk):
    if request.method == 'GET':
        marca = Marca.objects.get(pk=pk)
        marca_form = MarcaForm(instance=marca)
        return render(request, 'editarMarca.html', {'form': marca_form,'id':marca.pk})
    else:
        marca_editar = Marca.objects.get(pk=pk)
        marca_form = MarcaForm(request.POST, request.FILES,instance=marca_editar)
        if marca_form.is_valid():
            marca_form.save()
            # return HttpResponse('Guardado correctamente')
            return redirect('listadoMarcas')

DEFAULT_MARCA_NOMBRE = ''
DEFAULT_MARCA_CANTIDAD = 5
DEFAULT_MARCA_ORDEN = 'nombre'

DEFAULT_ARTICULO_ORDEN = 'articulo_marca__nombre'
DEFAULT_ARTICULO_CANTIDAD = 5
def articulosParaComprador(request):
    # articulos = Articulo.objects.all()
    todasLasMarcas = Marca.objects.order_by('nombre')
    todasLasPaginas = Paginator(todasLasMarcas, 3)
    page = request.GET.get('page')
    try:
        marcas = todasLasPaginas.page(page)
    except PageNotAnInteger:
        page=1
        # If page is not an integer, deliver first page.
        marcas = todasLasPaginas.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        marcas = todasLasPaginas.page(todasLasPaginas.num_pages)
    if request.is_ajax():
            # data = serializers.serialize("json", articulos)
            data = map(lambda x: x.what_i_need_in_ajax_call_for_marca(),  marcas)
            return HttpResponse(json.dumps({
                                    "marcas": list(data),
                                    "cantPaginas": todasLasPaginas.num_pages,
                                    "page": page}),
                   content_type='application/json')
    return render(request, 'articulosParaComprador.html', {'marcas':marcas,"cantidadPaginas": todasLasPaginas.num_pages,
                                    "paginaActual": page})

@login_required(login_url='login.html')
def listadoArticulos(request):
    filtroMarca = request.GET.get('filtroMarca')
    filtroModelo = request.GET.get('filtroModelo')
    filtroDescripcion = request.GET.get('filtroDescripcion')
    filtrofechaDesde = request.GET.get('filtrofechaDesde')
    filtroFechaHasta = request.GET.get('filtroFechaHasta')
    cantidad = request.GET.get('cantidad', DEFAULT_ARTICULO_CANTIDAD)
    orden = request.GET.get('orden', DEFAULT_ARTICULO_ORDEN)
    todosLosArticulos = Articulo.objects.order_by(orden)
    if(filtroMarca is not None):
        todosLosArticulos = todosLosArticulos.filter(articulo_marca__nombre__icontains=filtroMarca)
    if(filtroModelo is not None):
        todosLosArticulos = todosLosArticulos.filter(modelo__icontains=filtroModelo)
    if(filtroDescripcion is not None):
        todosLosArticulos = todosLosArticulos.filter(descripcion__icontains=filtroDescripcion)
    if( (filtrofechaDesde is not None) & (filtroFechaHasta is not None)):
        todosLosArticulos = todosLosArticulos.filter(fecha__range=(filtrofechaDesde, filtroFechaHasta))

    todasLasPaginas = Paginator(todosLosArticulos, cantidad)
    page = request.GET.get('page')
    try:
        articulos = todasLasPaginas.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page=1
        articulos = todasLasPaginas.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articulos = todasLasPaginas.page(todasLasPaginas.num_pages)
    if request.is_ajax():
            # data = serializers.serialize("json", articulos)
            data = map(lambda x: x.what_i_need_in_ajax_call_for_articulo(),  articulos)
            return HttpResponse(json.dumps({
                                    "articulos": list(data),
                                    "cantPaginas": todasLasPaginas.num_pages,
                                    "page": page,
                                    "orden": orden}),
                   content_type='application/json')
    return render(request, 'listadoArticulos.html', {'articulos':articulos,'cantidadPaginas':todasLasPaginas.num_pages,
                                                      'paginaActual':page})

def date_handler(obj): #USADO PARA SERIALIZAR FECHA EN JSON
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

@login_required(login_url='login.html')
def listadoMarcas(request):
        nombre = request.GET.get('nombre', DEFAULT_MARCA_NOMBRE)
        cantidad = request.GET.get('cantidad', DEFAULT_MARCA_CANTIDAD)
        orden = request.GET.get('orden', DEFAULT_MARCA_ORDEN)
        todasLasMarcas = Marca.objects.filter(nombre__icontains=nombre).order_by(orden)  #la 'i' antes del contains lo hace no case sensitive
        todasLasPaginas = Paginator(todasLasMarcas, cantidad)
        page = request.GET.get('page')
        try:
            marcas = todasLasPaginas.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page=1
            marcas = todasLasPaginas.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            marcas = todasLasPaginas.page(todasLasPaginas.num_pages)
            # if request.is_ajax():
            #HACER ALGO
        if request.is_ajax():
            data = serializers.serialize("json", marcas)
            # cantPaginas = todasLasPaginas.num_pages
            return HttpResponse(json.dumps({
                                    "marcas": data,
                                    "cantPaginas": todasLasPaginas.num_pages,
                                    "page": page,
                                    "orden": orden}),
                   content_type='application/json')
        return render(request, 'listadoMarcas.html', {'marcas':marcas,'cantidadPaginas':todasLasPaginas.num_pages,
                                                      'paginaActual':page})


@login_required(login_url='login.html')
def crear_marca(request):
    if request.method == 'POST':
        marca_form = MarcaForm(request.POST, request.FILES)
        if marca_form.is_valid():
            marca = marca_form.save()
            # return HttpResponse('Guardado correctamente')
            return redirect('listadoMarcas')
    else:
        marca_form = MarcaForm()

    return render(request, 'crearMarca.html', {'form': marca_form})

@login_required(login_url='login.html')
def crear_articulo(request):
    if request.method == 'POST':
        articulo_form = ArticuloForm(request.POST, request.FILES)
        if articulo_form.is_valid():
            articulo_form.save()
            # return HttpResponse('Guardado correctamente')
            return redirect('listadoArticulos')
    else:
        articulo_form = ArticuloForm()

    return render(request, 'crearArticulo.html', {'form': articulo_form})

def login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                auth_login(request, user)
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                return redirect('listadoArticulos')
            else:
                # An inactive account was used - no logging in!
                return render(request, 'login.html', {'mensaje':'Cuenta inhabilitada'})
        else:
            # Bad login details were provided. So we can't log the user in.
            return render(request, 'login.html', {'mensaje':'Datos invalidos'})

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html')

def register(request):
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            registered = True
            user_auth = authenticate(username=user.username, password=user.password)
            if user_auth:
                # Is the account active? It could have been disabled.
                if user_auth.is_active:
                    # If the account is valid and active, we can log the user in.
                    # We'll send the user back to the homepage.
                    auth_login(request, user_auth)
                    # return render(request, 'index.html')

        else:
            print (user_form.errors)

    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request,
            'register.html',
            {'user_form': user_form, 'registered': registered})

def logout_view(request):
    logout(request)
    return redirect('index')
