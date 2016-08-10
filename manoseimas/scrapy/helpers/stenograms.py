# coding: utf-8

from __future__ import unicode_literals

import re
import difflib
import datetime
import operator

from manoseimas.scrapy import models

clean_words_re = re.compile(r'ir|svarstymas|pateikimas|priėmimas')
clean_title_re = re.compile(r'[()[\]„“",  ]+')


def get_voting_for_stenogram(votings, title, dt):
    """Find voting for stenogram by stenogram topic title and datetime

    Parameters:
    - votings: queryset of compatibility_test.Voting objects
    - title: str, stenogram topic title
    - dt: datetime.datetime, stenogram topic date and time

    Returns: generator with docs matching given title and datetime

    """

    def clean_title(title):
        result = title.lower()
        result = clean_words_re.sub(' ', result)
        result = clean_title_re.sub(' ', result)
        return result

    title = clean_title(title)
    votings_by_ratio = []
    for voting in votings:
        _dt = voting.timestamp
        _title = clean_title(' '.join([d['name'] for d in voting.value['documents']]))
        ratio = difflib.SequenceMatcher(None, title, _title).ratio()
        votings_by_ratio.append((ratio, abs(_dt - dt), voting))

    allowed_time_delta = datetime.timedelta(minutes=30)
    if votings_by_ratio:
        # Sort by delta asc and ratio desc
        votings_by_ratio.sort()
        votings_by_ratio.sort(key=operator.itemgetter(0), reverse=True)

        for ratio, delta, doc in votings_by_ratio:
            if ratio > 0.9 and delta < allowed_time_delta:
                yield doc

            # If both ratio and delta are out of range, do not check the
            # others.
            if not (ratio > 0.9 or delta < allowed_time_delta):
                break


def get_votings_by_date(date):
    assert isinstance(date, datetime.date)
    return models.Voting.objects.filter(timestamp__range=(
        datetime.datetime.combine(date, datetime.time.min),
        datetime.datetime.combine(date, datetime.time.max),
    ))
