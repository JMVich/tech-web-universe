from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from PedidosApp.models import Pedido, LineaPedido
from CarroApp.carro import Carro
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
import stripe

# Create your views here.

@login_required(login_url = "/autenticacion/logear")   #este deco. hace que si no está logueado, se pasa por pará. la url a la que se redirigirá.
def postprocesarpedido(request):          #esto se crea mediante el boton de realizar pedido.
    pedido = Pedido.objects.create(user = request.user)
    carro = Carro(request)
    lineas_pedido = list()    #esta lista la almacenamos en la BD mas abajo.

    for key, value in carro.carro.items():     #debemos recorrer el carro con un bucle fpr para poder visualizarlo.
        lineas_pedido.append(LineaPedido(      #esto es para que agregue lo que declaré dentro del modelo de LineaPedido.

            producto_id = key,
            cantidad = value["cantidad"],
            user = request.user,
            pedido = pedido 

        ))

    LineaPedido.objects.bulk_create(lineas_pedido)   #esto realiza los insert into en la BD.

    enviar_mail(                #este será el mail que se le enviará al usuario, la función se crea más adelante.
        pedido = pedido,
        lineas_pedido = lineas_pedido,
        nombreusuario = request.user.username,
        emailusuario = request.user.email
    )

    messages.success(request, "El pedido ha creado correctamente")    #luego, se envía este msg.

    return render(request, 'pedidos/gracias.html')   #esto es para que cuando termine, te rediriga a la tienda nuevamente.


def enviar_mail(**kwargs):  #esto es para que reciba un n indeterminado de campos (son 4, pero porlas dudas).
    asunto = "Gracias por el pedido"
    mensaje = render_to_string("emails/pedido.html",{

        "pedido": kwargs.get("pedido"),
        "lineas_pedido": kwargs.get("lineas_pedido"),
        "nombreusuario": kwargs.get("nombreusuario"),

    })

    mensaje_texto = strip_tags(mensaje)   #esto es para omitir etiquetas html?.

    from_email = "juanviscovich14@gmail.com"
    #to = kwargs.get("emailusuario")
    to = "juanmaviscovich@hotmail.com"

    send_mail(asunto, mensaje_texto, from_email, [to], html_message=mensaje)


def procesar_pedido(request):

    if request.method == 'POST':
        # Obtener el token de pago enviado por Stripe
        token = request.POST.get('stripeToken')

        try:
            # Configurar la API de Stripe con tu clave secreta
            stripe.api_key = 'sk_test_51NgXjZBjXHxUKBZ4bBlNaOcZ56HbAPFUKxh744mNm4JU2xmT67QLBCtijMtISvBCe5X64ya3MpnGWMqWbUUr9Rhm00uBkl5SW0'

            # Crear un cargo en Stripe
            charge = stripe.Charge.create(
                amount=1000,  # El monto en centavos
                currency='usd',  # La moneda
                description='Pago de pedido',
                source=token  # El token de pago
            )

            # Si el cargo fue exitoso, redirigir a la página de agradecimiento
            return redirect('postprocesarpedido')

        except stripe.error.CardError as e:
            # En caso de error con la tarjeta, mostrar un mensaje al usuario
            messages.error(request, f"Error en el pago: {e.error.message}")
            #return redirect('proceso_pago')

    # Si la solicitud no es POST, simplemente renderiza la página de pago
    return render(request, 'pedidos/pedidos.html')
