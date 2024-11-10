from django import template

register = template.Library()

@register.filter
def formato_precio(value):
    """ Formatear el precio como $1.000,00 """
    try:
        value = float(value)
        return f"{value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return value
