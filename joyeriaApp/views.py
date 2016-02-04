from django.shortcuts import render,render_to_response,redirect
from .forms import ArticuloForm,MarcaForm
from django.http import *
from django.contrib.auth.forms import UserCreationForm
from .models import Marca,Articulo
from django.template import loader,RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout

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
            art = articulo_form.save(commit=False)
            art.save()
            return HttpResponse('Guardado correctamente')
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
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
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
        user_form = UserCreationForm(data=request.POST)

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
        user_form = UserCreationForm()

    # Render the template depending on the context.
    return render(request,
            'register.html',
            {'user_form': user_form, 'registered': registered})

def logout_view(request):
    logout(request)
    return redirect('index')