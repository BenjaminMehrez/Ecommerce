from django import template

register = template.Library()

@register.filter
def pluralize_es(count, singular_plural):
    """
    Filtra para pluralizar en español.
    Usage: {{ count|pluralize_es:"vendedor,vendedores" }}
    """
    singular, plural = singular_plural.split(',')
    return singular if count == 1 else plural
