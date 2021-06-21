from django import template

register = template.Library()

def panel_to_column_size(value): # Only one argument.
    dic = {'S': 4, 'M': 6, 'L': 12}
    return dic[value]

register.filter('panel_to_column_size', panel_to_column_size)


def none_to_empty_str(value):
    if value == None:
        return ''
    else:
        return value

register.filter('none_to_empty_str', none_to_empty_str)