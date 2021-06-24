from django import template

register = template.Library()

# converts panel.panel_size value ('s','m','l') to appropriate bootstrap column sizes (4,6,12)
def panel_to_column_size(value): 
    dic = {'S': 4, 'M': 6, 'L': 12}
    return dic[value]

register.filter('panel_to_column_size', panel_to_column_size)

# returns value to be used in template inline style as font size of element according to boostrap column size per panel size, used only for tables in certain templates
def dynamic_font_size(value):
    dic = {'S': 4, 'M': 6, 'L': 12}
    return str(dic[value]*0.06)
register.filter('dynamic_font_size', dynamic_font_size)


# returns value to be used in template inline style as height of element according to boostrap column size per panel size, used only for tables in certain templates
def elem_height(value):
     dic = {'S': 4, 'M': 6, 'L': 12}
     return str(dic[value] * 0.06)

register.filter('elem_height', elem_height)

# returns 'danger' if message.tags is 'error', to use alert-danager bootstrap class in template in that case, used in template for bootstrap style
def message_to_bootstrap(value):
    dic = {'error': 'danger'}
    if value not in dic:
        return value
    else:
        return dic[value]
register.filter('message_to_bootstrap', message_to_bootstrap)

# utilized on public peer user pages.  returns value in quotes if value is a string
def make_quote(value):
    if type(value) == str:
        return f"\"{value}\""
    else:
        pass

register.filter('make_quote', make_quote)

# utilized on public peer user pages. if there is no bio available, return appropriate string
def no_bio(value):
    if not value:
        return "No bio available yet"
    else:
        return value
register.filter('no_bio', no_bio)



