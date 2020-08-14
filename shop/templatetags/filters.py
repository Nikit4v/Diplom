from django import template

register = template.Library()


@register.filter
def to_stars(num: int) -> str:
    return "★" * num + "✰" * (5 - num)
