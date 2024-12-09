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
			"title": f"{item.qty}x {item.item}",
			"picture_url": item.image,
			"quantity": item.qty,
			"description": item.size,
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

    if settings.ENVIRONMENT == 'production':
        preference_data = {
            "items": items,
            "back_urls": {
                "success": f"http://ecommercemehrez.up.railway.app/ ent-success/{order.oid}",
                "failure": "http://ecommercemehrez.up.railway.app/payment-failed/",
                "pending": "http://ecommercemehrez.up.railway.app/payment-pending/",
            },
            "auto_return": "approved",
            "external_reference": str(order.oid),  # ID único para identificar el pedido
            "statement_descriptor": "Ecommerce Mehrez",
        }
    else:
        preference_data = {
            "items": items,
            "back_urls": {
                "success": f"https://65f0-2803-9800-9844-7592-65cb-d993-ef4c-c86b.ngrok-free.app/payment-success/{order.oid}",
                "failure": "https://65f0-2803-9800-9844-7592-65cb-d993-ef4c-c86b.ngrok-free.app/payment-failed/",
                "pending": "https://65f0-2803-9800-9844-7592-65cb-d993-ef4c-c86b.ngrok-free.app/payment-pending/",
            },
            "auto_return": "approved",
            "external_reference": str(order.oid),  # ID único para identificar el pedido
            "statement_descriptor": "Ecommerce Mehrez Test",
        }
        

    preference = sdk.preference().create(preference_data)
    return preference["response"]

