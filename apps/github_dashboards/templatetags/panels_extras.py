from django import template

register = template.Library()

# converts panel.panel_size value ('s','m','l') to appropriate bootstrap column sizes (4,6,12)
def panel_to_column_size(value): 
    dic = {'S': 4, 'M': 6, 'L': 12}
    return dic[value]

register.filter('panel_to_column_size', panel_to_column_size)

# utilized for dynamically sizing fontsize and tr,th height within tables (only in certain templates) based upon table.panel_size, returns value to be used in template inline style  according to boostrap column size per panel size
def resize_from_columns(value):
    dic = {'S': 4, 'M': 6, 'L': 12}
    return str(dic[value]*0.12)
register.filter('resize_from_columns', resize_from_columns)

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



# {% block othercss %}
# <link href="https://languages.abranhe.com/logos.css" rel="stylesheet">
# {% endblock othercss %}