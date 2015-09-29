from django.contrib import admin

from .models import Lobbyist


class LobbyistAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


admin.site.register(Lobbyist)
