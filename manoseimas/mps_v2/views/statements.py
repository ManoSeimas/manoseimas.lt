from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from manoseimas.mps_v2.models import ParliamentMember, Stenogram, StenogramStatement


def _statement_context(statement, highlighted=False):
    return {
        'id': statement.id,
        'speaker_id': statement.speaker.id if statement.speaker else None,
        'speaker_slug': statement.speaker.slug if statement.speaker else None,
        'speaker_name': statement.get_speaker_name(),
        'as_chairperson': statement.as_chairperson,
        'text': statement.text,
        'selected': highlighted,
    }


def _build_discussion_context(request, statement_id, selected_id=None):
    statement_qs = StenogramStatement.objects.select_related(
        'topic',
        'speaker').prefetch_related('topic__votings')
    statement = statement_qs.get(pk=statement_id)

    statements = statement.topic.statements.select_related('speaker').all()

    context = {
        'topic': {
            'id': statement.topic.id,
            'title': statement.topic.title,
            'timestamp': statement.topic.timestamp,
        },
        'selected_statement': _statement_context(statement),
        'statements': [
            _statement_context(stmt,
                               highlighted=(stmt.id == statement.id))
            for stmt in statements
        ],
    }
    return context


def mp_discussion(request, statement_id):
    context = _build_discussion_context(request, statement_id)
    return render(request, 'discussion.jade', context)


def mp_statements(request, mp_slug, statement_page=None):
    mp = ParliamentMember.objects.get(slug=mp_slug)

    selected_session = request.GET.get('session')
    only_as_presenter = request.GET.get('only_as_presenter')
    sessions = Stenogram.objects.distinct().values_list('session', flat=True)

    all_statements = StenogramStatement.objects.select_related(
        'topic').filter(speaker=mp,
                        as_chairperson=False).order_by('-topic__timestamp',
                                                       '-pk')
    if selected_session:
        all_statements = all_statements.filter(
            topic__stenogram__session=selected_session)
    if only_as_presenter:
        all_statements = all_statements.filter(topic__presenters=mp)

    statement_paginator = Paginator(all_statements, 10)
    try:
        statements = statement_paginator.page(statement_page)
    except PageNotAnInteger:
        statements = statement_paginator.page(1)
    except EmptyPage:
        statements = statement_paginator.page(statement_paginator.num_pages)

    context = {
        'statements': statements,
        'sessions': sessions,
        'selected_session': selected_session
    }

    return render(request, 'statments.jade', context)
