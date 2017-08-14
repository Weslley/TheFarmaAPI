from django import template
import markdown2

register = template.Library()


@register.filter(name='addclass')
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='addplaceholder')
def addplaceholder(field, value):
    return field.as_widget(attrs={"placeholder": value})


@register.filter(name='addplaceclass')
def addplaceclass(field, value):
    values = value.split('|')
    return field.as_widget(attrs={"placeholder": values[0], "class": values[1]})


@register.filter(name='moreone')
def moreone(value):
    return int(value) + 1


@register.filter(name='get_at_index')
def get_at_index(iterr, index):
    return iterr[index]


@register.filter(name='money_format')
def money_format(value):
    import locale
    locale.setlocale(locale.LC_ALL, '')
    return locale.format('%.2f', value, 1)


@register.filter(name='hasattr')
def hasattr(obj, value):
    return True


@register.filter
def get_range(value):
    return range(value)


@register.filter(name='from_markdown')
def from_markdown(value):
    return markdown2.markdown(value)
