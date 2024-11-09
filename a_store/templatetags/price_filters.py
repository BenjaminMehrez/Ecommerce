from django import template

register = template.Library()

@register.filter
def formato_precio(value):
    """ Formatear el precio como $1.000 sin decimales """
    try:
        # Convertir a float y redondear para eliminar decimales
        value = round(float(value))
        # Formatear como moneda argentina
        return f"{value:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return value
