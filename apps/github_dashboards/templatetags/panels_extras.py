from django import template

register = template.Library()

def panel_to_column_size(value): # Only one argument.
    dic = {'S': 4, 'M': 6, 'L': 12}
    return dic[value]

register.filter('panel_to_column_size', panel_to_column_size)


def de_none(value):
    if value == None:
        return ''

register.filter('de_none', de_none)