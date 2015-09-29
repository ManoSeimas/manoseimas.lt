from django.contrib import admin

from .models import Lobbyist


class LobbyistAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'source', 'raw_data')


admin.site.register(Lobbyist, LobbyistAdmin)
