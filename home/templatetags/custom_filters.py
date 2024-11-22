from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def filter_gte(value, arg):
    return [x for x in value if float(x['score']) >= arg]

@register.filter
def filter_lt(value, arg):
    return [x for x in value if float(x['score']) < arg]

@register.filter
def multiply(value, arg):
    return float(value) * float(arg)

@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0