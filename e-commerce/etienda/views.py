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
            <li><a href="C1">C1</a></li>
            <li><a href="C2">C2</a></li>
            <li><a href="C3">C3</a></li>
            <li><a href="C4">C4</a></li>
            <li><a href="C5">C5</a></li>
            <li><a href="C6">C6</a></li>
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