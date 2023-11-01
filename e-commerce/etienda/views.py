from django.shortcuts import render
from django.views.static import serve
from django.conf import settings

# Create your views here.
from django.http import HttpResponse

from . import models
from . import forms

def index(request):
    context = {'productos' : models.ObtenerProductos(), 'categorias' : models.ObtenerCategorias()}
    return render(request, 'etienda/index.html', context)

def busqueda(request):
    context = {'search_query' : request.GET.get('input_busqueda', ''), 'productos' : models.ObtenerProductosConcretos(request.GET.get('input_busqueda', '')), 'categorias' : models.ObtenerCategorias()}
    return render(request, 'etienda/busqueda.html', context)

def categoria(request, categoria):
    context = {'productos' : models.ObtenerProductosCategoria(categoria), 'categorias' : models.ObtenerCategorias(), 'categoria' : categoria}
    return render(request, 'etienda/categoria.html', context)

def añadir(request):
    context = {'form' : forms.ProductoForm(), 'categorias' : models.ObtenerCategorias()}
    return render(request, 'etienda/add.html', context)