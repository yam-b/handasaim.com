from django import template

register = template.Library()


@register.filter
def column(value, index):
    return [row[index] for row in value[1:] if row[index]]
