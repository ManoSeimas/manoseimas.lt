from django.contrib import admin

from . import models


class LobbyistAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'source', 'modified_at', 'raw_data')


admin.site.register(models.Lobbyist, LobbyistAdmin)
admin.site.register(models.LobbyistDeclaration)
admin.site.register(models.LobbyistClient)
admin.site.register(models.LobbyistLawProject)
