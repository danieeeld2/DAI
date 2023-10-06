from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    html = """
    <html>
    <header></header>
    <body>
        <h1>Consultas a la BD</h1>
        <ul>
            <li><a href="C1">Electrónica entre 100 y 200 euros, ordenados por precio</a></li>
            <li><a href="C2">Productos que contengas la palabra pocket en la descripción</a></li>
            <li><a href="C3">Productos con puntuación mayor de 4</a></li>
            <li><a href="C4">Rompa de hombre, ordenada por puntuación</a></li>
            <li><a href="C5">Facturación total</a></li>
            <li><a href="C6">Facturación por categoria de producto</a></li>
        </ul>
    </body>
    </html>
    """
    return HttpResponse(html)
def C1(request):
    return HttpResponse()
def C2(request):
    return HttpResponse()
def C3(request):
    return HttpResponse()
def C4(request):
    return HttpResponse()
def C5(request):
    return HttpResponse()
def C6(request):
    return HttpResponse()