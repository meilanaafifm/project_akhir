"""
Custom template tags untuk akademik app
"""

from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Filter untuk mengakses dictionary dengan key"""
    if dictionary:
        return dictionary.get(key, 0)
    return 0
