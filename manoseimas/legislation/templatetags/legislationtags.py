from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.inclusion_tag('manoseimas/legislation/templatetags/menu.html',
                        takes_context=True)
def legislation_menu(context):
    legislation_number = context['legislation'].number
    urls = [
        ('legislation', _(u'Įstatymas'),
         reverse('manoseimas-legislation', args=[legislation_number])),

        ('amendments', _(u'Pataisos'),
         reverse('manoseimas-legislation-amendments',
                 args=[legislation_number])),

        ('drafts', _(u'Projektai'), '#'),
    ]

    active = context.get('legislation_active_page', 'legislation')
    menu = []
    for key, title, url in urls:
        item = {
            'url': url,
            'title': title,
            'is_active': key == active,
        }
        menu.append(item)

    return {
        'legislation_menu': menu,
    }
