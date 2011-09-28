from django import template

from manoseimas.search.forms import SearchForm

register = template.Library()


@register.inclusion_tag('manoseimas/search/templatetags/search_form.html',
                        takes_context=True)
def search_form(context):
    request = context['request']
    if 'query' in request.GET:
        search_form = SearchForm(data=request.GET)
    else:
        search_form = SearchForm()

    return {
        'search_form': search_form,
    }
