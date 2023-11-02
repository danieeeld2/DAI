from django.shortcuts import render
from django.views.static import serve
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)

# Create your views here.
from django.http import HttpResponse
from django.contrib import messages 

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
    if request.method == 'POST':
        form = forms.ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = {
                'title' : form.cleaned_data['title'],
                'category' : form.cleaned_data['category'],
                'description' : form.cleaned_data['description'],
                'price' : form.cleaned_data['price'],
                'image' : form.cleaned_data['image']
            }

            # Copiar el archivo a static/imagenes e imagenes/
            image_path = form.cleaned_data['image'].name
            destination1 = os.path.join('imagenes', image_path)
            with open(destination1, 'wb') as destination_file:
                for chunk in form.cleaned_data['image'].chunks():
                    destination_file.write(chunk)
            destination2 = os.path.join('static/imagenes', image_path)
            with open(destination2, 'wb') as destination_file:
                for chunk in form.cleaned_data['image'].chunks():
                    destination_file.write(chunk)
                    
            producto['image'] = destination1
            logger.info('Añadiendo producto %s', producto)

            models.AñadirProducto(producto)
            logger.info('Añadido producto %s', producto)
            messages.success(request, 'Product added successfully.')

            return render(request, 'etienda/add.html', {'form': forms.ProductoForm(), 'categorias' : models.ObtenerCategorias()})
        
        else:
            form.add_error('title', 'Title must begin with a capital letter')
            logger.error('Error añadiendo producto')
            messages.warning(request, 'Something went wrong. Please try again.')
            return render(request, 'etienda/add.html', {'form': form, 'categorias' : models.ObtenerCategorias()})
        
    # Predeterminado   
    context = {'form' : forms.ProductoForm(), 'categorias' : models.ObtenerCategorias()}
    return render(request, 'etienda/add.html', context)