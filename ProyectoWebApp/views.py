from django.shortcuts import render, HttpResponse
from CarroApp.carro import Carro

# Create your views here.


def home(request):

    carro = Carro(request)

    return render(request, "ProyectoWebApp/home.html")

def legal(request):
    return render(request, "ProyectoWebApp/legal.html")