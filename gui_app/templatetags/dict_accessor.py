from django import template
register = template.Library()


@register.filter(name='get_value')
def get_value(dictionary, key):
    return dictionary[key]


@register.filter(name='get_description')
def get_description(dictionary):
    if 'description' in dictionary:
        return dictionary['description']
    elif 'Description' in dictionary:
        return dictionary['Description']
    else:
        return ""
