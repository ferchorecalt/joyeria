from django.shortcuts import render,render_to_response,redirect
from .forms import ArticuloForm,MarcaForm,UserForm
from django.http import *
from .models import Marca,Articulo
from django.template import loader,RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

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
                login(request, user)
                return HttpResponseRedirect('login.html') #habria que ver que hacer aca
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
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print (user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'registered': registered},
            context)