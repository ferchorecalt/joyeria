from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^gallery', views.index, name='index'),
    url(r'^404', views.index, name='index'),
    url(r'^news', views.index, name='index'),
    url(r'^mail', views.index, name='mail'),
]