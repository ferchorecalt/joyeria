from django.shortcuts import render,render_to_response,redirect
from .forms import ArticuloForm,MarcaForm,UserForm,ContactForm
from django.http import *
from .models import Marca,Articulo
from django.template import loader,RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
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
    # return render(request, 'mail.html')
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            nombre = request.POST.get('nombre', '')
            mail = request.POST.get('mail', '')
            asunto = request.POST.get('asunto', '')
            mensaje = request.POST.get('mensaje', '')

            # Email the profile with the
            # contact information
            template =get_template('contact_template.txt')
            context = Context({
                'nombre': nombre,
                'mail': mail,
                'asunto': asunto,
                'mensaje': mensaje,
            })
            content = template.render(context)

            email = EmailMessage(
                asunto,
                content,
                mail,
                ['ilanrosenfeld7@gmail.com'],
                headers = {'Reply-To': mail }
            )
            email.send()
            return redirect('mail')
    return render(request, 'mail.html', {
        'form': form_class,
    })

def single(request):
    return render(request, 'single.html')

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

@login_required(login_url='login.html')
def listadoArticulos(request):
    articulos = Articulo.objects.all()
    return render(request, 'listadoArticulos.html', {'articulos':articulos})

@login_required(login_url='login.html')
def listadoMarcas(request):
    marcas = Marca.objects.all()
    return render(request, 'listadoMarcas.html', {'marcas':marcas})

@login_required(login_url='login.html')
def crear_marca(request):
    if request.method == 'POST':
        marca_form = MarcaForm(request.POST)
        if marca_form.is_valid():
            marca = marca_form.save()
            # return HttpResponse('Guardado correctamente')
            marca_form=MarcaForm()
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
