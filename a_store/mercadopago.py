import mercadopago
from django.conf import settings
import uuid


def create_preference(order):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {
        'x-idempotency-key': str(uuid.uuid4())  # Genera un UUID único
    }

    # Convertir los elementos del pedido a items de Mercado Pago
    items = [
        {
			"title": item.item,
			"picture_url": item.image,
			"quantity": item.qty,
			"currency_id": "ARS",
			"unit_price": float(item.price),
        }
        for item in order.cartorderitems_set.all()
    ]

    # Agregar un ítem con el descuento
    if order.saved > 0:
        items.append({
            "title": "Descuento aplicado",
            "quantity": 1,
            "currency_id": "ARS",
            "unit_price": -float(order.saved),  # Descuento como valor negativo
        })

    preference_data = {
        "items": items,
        "back_urls": {
            "success": "http://ecommercemehrez.up.railway.app/payment-success/",
            "failure": "http://ecommercemehrez.up.railway.app/payment-failed/",
            "pending": "http://ecommercemehrez.up.railway.app/payment-pending/",
        },
        "auto_return": "approved",
        "external_reference": str(order.oid),  # ID único para identificar el pedido
        "statement_descriptor": "Test Ecommerce",
    }

    preference = sdk.preference().create(preference_data)
    return preference["response"]

