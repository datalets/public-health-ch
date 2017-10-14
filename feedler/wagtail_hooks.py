# -*- coding: utf-8 -*-

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from .admin import EntryModelAdminMixin
from .models import Entry, Stream

class EntryModelAdmin(EntryModelAdminMixin, ModelAdmin):
    model = Entry
    menu_icon = 'date'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_filter = ('author', 'tags')
    list_display = ('published', 'title', 'with_image', 'lang')
    search_fields = ('title', 'author', 'content', 'tags')

modeladmin_register(EntryModelAdmin)

class StreamModelAdmin(ModelAdmin):
    model = Stream
    menu_icon = 'date'
    menu_order = 1000
    add_to_settings_menu = True
    exclude_from_explorer = True
    list_display = ('title', 'ident')

modeladmin_register(StreamModelAdmin)
