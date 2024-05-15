from django.shortcuts import render

from TiendaApp.models import Producto, CategoriaProd

# Create your views here.

def tienda(request):

    productos = Producto.objects.all()

    return render(request, "tienda/tienda.html", {"productos": productos})
