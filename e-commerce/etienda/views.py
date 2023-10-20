from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from . import models

def index(request):
    context = {}
    return render(request, 'etienda/index.html', context)

def busqueda(request):
    context = {'search_query' : request.GET.get('input_busqueda', '')}
    return render(request, 'etienda/busqueda.html', context)