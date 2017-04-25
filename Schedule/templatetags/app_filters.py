from django import template

register = template.Library()


@register.filter
def column(value, index):
    lst=[]
    for row in value[1:]:
        a=row[2]
        if a:
            lst.append(a)
    return lst