from django.shortcuts import render

from ServiciosApp.models import Servicio

# Create your views here.

def servicios(request):
    servicios = Servicio.objects.all()
    return render(request, "servicios/servicios.html", {"servicios": servicios})