from django import template

register = template.Library()

@register.filter
def float_dot(value):
    try:
        return f'{float(value):.2f}'.replace(',', '.')
    except (ValueError, TypeError):
        return value
