from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

from .api import api

urlpatterns = [
    path("", views.index, name="index"),
    path("buscar", views.busqueda, name="busqueda"),
    path("buscar-categoria/<str:categoria>/", views.categoria, name="categoria"),
    path("add", views.añadir, name="add"),
]
