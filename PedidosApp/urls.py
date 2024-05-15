from django.urls import path
from . import views

urlpatterns = [
    # ... tus otras URLs ...

    # URL para la vista de procesar_pedido
    path('procesar_pedido/', views.procesar_pedido, name='procesar_pedido'),

    # URL para la vista de postprocesarpedido
    path('postprocesarpedido/', views.postprocesarpedido, name='postprocesarpedido'),
]


