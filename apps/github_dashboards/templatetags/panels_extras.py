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


def no_bio(value):
    if not value:
        return "No bio available yet"
    else:
        return value
register.filter('no_bio', no_bio)


def make_quote(value):
    if type(value) == str:
        return f"\"{value}\""
    else:
        pass

register.filter('make_quote', make_quote)

def message_to_boostrap(value):
    dic = {'error': 'danger'}
    if value not in dic:
        return value
    else:
        return dic[value]
register.filter('message_to_boostrap', message_to_boostrap)