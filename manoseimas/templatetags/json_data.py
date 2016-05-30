from django import template
from django.utils.safestring import mark_safe

import json
from rest_framework.renderers import JSONRenderer

register = template.Library()


@register.simple_tag(takes_context=False)
def to_json(data_dict):
    return mark_safe(JSONRenderer().render(data_dict))


@register.filter(is_safe=True)
def dict_to_json(obj):
    if hasattr(obj, 'to_dict'):
        obj = obj.to_dict()
    return mark_safe(json.dumps(obj))
