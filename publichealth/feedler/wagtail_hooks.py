# -*- coding: utf-8 -*-

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from .models import Entry

class EntryModelAdmin(ModelAdmin):
    model = Entry
    menu_icon = 'date'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ('updated', 'title', 'origin_title', 'tags')
    # list_filter = ('origin_title')
    # search_fields = ('title', 'origin_title', 'content', 'tags')

modeladmin_register(EntryModelAdmin)
