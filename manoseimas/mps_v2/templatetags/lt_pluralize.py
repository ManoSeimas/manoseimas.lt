from django import template

register = template.Library()


@register.simple_tag
def lt_pluralize(n, singular, plural1, plural2):
    if n is None or n is '' or n is u'':
        return plural2
    n = int(n)
    if n % 10 == 1 and n % 100 != 11:
        return singular
    elif n % 10 >= 2 and (n % 100 < 10 or n % 100 >= 20):
        return plural1
    else:
        return plural2
