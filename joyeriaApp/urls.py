from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^gallery', views.gallery, name='gallery'),
    url(r'^404', views.services, name='services'),
    url(r'^news', views.news, name='news'),
    url(r'^mail', views.mail, name='mail'),
    url(r'^index', views.index, name='index'),
    url(r'^single/(?P<pk>\d+)$', views.single, name='single'),
    url(r'^singleMarca/(?P<pk>\d+)$', views.singleMarca, name='singleMarca'),
    url(r'^crearArticulo', views.crear_articulo, name='crearArticulo'),
    url(r'^crearMarca', views.crear_marca, name='crearMarca'),
    url(r'^login', views.login, name='login'),
    url(r'^register', views.register, name='register'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^listadoArticulos', views.listadoArticulos, name='listadoArticulos'),
    url(r'^listadoMarcas', views.listadoMarcas, name='listadoMarcas'),
    url(r'^eliminarArticulo/(?P<pk>\d+)$', views.eliminarArticulo, name='eliminarArticulo'),
    url(r'^editarArticulo/(?P<pk>\d+)$', views.editarArticulo, name='editarArticulo'),
    url(r'^eliminarMarca/(?P<pk>\d+)$', views.eliminarMarca, name='eliminarMarca'),
    url(r'^editarMarca/(?P<pk>\d+)$', views.editarMarca, name='editarMarca'),
    url(r'^articulosParaComprador', views.articulosParaComprador, name='articulosParaComprador'),
]
