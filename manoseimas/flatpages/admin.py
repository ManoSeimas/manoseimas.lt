from django.contrib import admin

from .models import FlatPage

class FlatPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    change_form_template = 'flatpage/admin.jade'

admin.site.register(FlatPage, FlatPageAdmin)
