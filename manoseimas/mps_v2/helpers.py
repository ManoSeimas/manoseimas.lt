# coding: utf-8

from __future__ import division
from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from manoseimas.compatibility_test.models import Topic


def _get_position_css_class(position):
    words = []
    abspos = abs(position)

    if abspos > 1.4:
        words.append('strong')
    elif abspos < 0.8:
        words.append('lite')

    if position > 0:
        words.append('support')
    else:
        words.append('against')

    return '-'.join(words)


def _get_topic_details(topic, position):
    percent = int(abs(position) / 2 * 100)
    return {
        'node_ref': topic.pk,
        'permalink': '#',  # we don't have topic page
        'formatted': (_('Palaiko %d%%') if position >= 0 else _('Nepalaiko %d%%')) % percent,
        'title': 'Aukštojo mokslo reforma',
        'position': 1.5,
        'klass': _get_position_css_class(position),
    }


def get_profile_positions(positions):
    if 'for' in positions:
        # preserve old positions format
        # see: https://github.com/ManoSeimas/manoseimas.lt/issues/154#issuecomment-231137335
        return positions

    result = {'for': [], 'against': [], 'neutral': []}
    topics = {x.pk: x for x in Topic.objects.filter(pk__in=positions.keys())}
    for topic_id, position in positions.items():
        topic_id = int(topic_id)
        position = float(position)
        if topic_id in topics:
            topic = topics[topic_id]
        else:
            continue
        if abs(position) < 0.2:
            result['neutral'].append(_get_topic_details(topic, position))
        elif position > 0:
            result['for'].append(_get_topic_details(topic, position))
        else:
            result['against'].append(_get_topic_details(topic, position))
    return result
