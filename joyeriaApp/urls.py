from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^gallery', views.gallery, name='gallery'),
    url(r'^404', views.services, name='services'),
    url(r'^news', views.news, name='news'),
    url(r'^mail', views.mail, name='mail'),
]