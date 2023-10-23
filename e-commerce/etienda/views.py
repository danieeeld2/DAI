from django.shortcuts import render
from django.views.static import serve
from django.conf import settings

# Create your views here.
from django.http import HttpResponse

from . import models

def index(request):
    context = {'productos' : models.ObtenerProductos(), 'categorias' : models.ObtenerCategorias()}
    return render(request, 'etienda/index.html', context)

def busqueda(request):
    context = {'search_query' : request.GET.get('input_busqueda', ''), 'productos' : models.ObtenerProductosConcretos(request.GET.get('input_busqueda', '')), 'categorias' : models.ObtenerCategorias()}
    return render(request, 'etienda/busqueda.html', context)
