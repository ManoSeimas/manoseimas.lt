from django.contrib import admin
from django.utils.html import format_html, format_html_join

from . import models


class LobbyistAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'source', 'modified_at', 'raw_data')


class LobbyistClientInline(admin.StackedInline):
    model = models.LobbyistClient
    extra = 0
    fields = ('_law_projects',)
    readonly_fields = ('_law_projects',)
    can_delete = False
    template = 'lobbyist_client_inline.html'

    def _law_projects(self, instance):
        return format_html(u'<ol style="clear: left">{}</ol>',
            format_html_join(
                '\n',
                u'<li>{}</li>',
                [(lp.title,) for lp in instance.law_projects.all()],
            ),
        )
    _law_projects.short_description = 'Law projects'
    _law_projects.allow_tags = True


class LobbyistDeclarationAdmin(admin.ModelAdmin):
    readonly_fields = ('source', 'modified_at', 'raw_data')
    inlines = (LobbyistClientInline,)


admin.site.register(models.Lobbyist, LobbyistAdmin)
admin.site.register(models.LobbyistDeclaration, LobbyistDeclarationAdmin)
