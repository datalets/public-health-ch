# -*- coding: utf-8 -*-
from django import template
from django.utils import translation

register = template.Library()

@register.simple_tag()
def language_cur():
    return translation.get_language()

# Language switcher
@register.inclusion_tag('tags/language.html', takes_context=True)
def language_switcher(context):
    url = '/$lang$'
    if 'page' in context:
        urlparts = context['page'].get_url_parts()
        if urlparts is not None:
            s, r, page_url_relative_to_site_root = urlparts
            url = page_url_relative_to_site_root.split('/')
            if len(url) > 0 and len(url[1]) == 2:
                url[1] = '$lang$'
                url = '/'.join(url)
            else:
                url = '/$lang$'
    language_array = [
        { 'code': 'de', 'title': 'De', 'url': url.replace('$lang$','de') },
        { 'code': 'fr', 'title': 'Fr', 'url': url.replace('$lang$','fr') },
        { 'code': 'en', 'title': 'En', 'url': url.replace('$lang$','en') }
    ]
    return {
        'languages': language_array,
        'currentlangcode': translation.get_language(),
        'request': context['request'],
    }

@register.simple_tag(takes_context=True)
def get_site(context):
    return context['request'].site

@register.simple_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return get_site(context).root_page

def has_menu_children(page):
    return page.get_children().live().in_menu().exists()

# Retrieves the top menu items
@register.inclusion_tag('tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().live().in_menu().specific()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.active = (calling_page.url.startswith(menuitem.url)
                           if calling_page else False)
        try:
            menuitem.title = menuitem.trans_title
        except AttributeError:
            pass
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        'request': context['request'],
    }

def menuitems_children(parent):
    menuitems_children = parent.get_children().live().in_menu().specific()
    for menuitem in menuitems_children:
        try:
            menuitem.title = menuitem.trans_title
        except AttributeError:
            pass
    return menuitems_children

# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent):
    return {
        'parent': parent,
        'menuitems_children': menuitems_children(parent),
        'request': context['request'],
    }

# Retrieves the footer menu items
@register.inclusion_tag('tags/footer_menu.html', takes_context=True)
def footer_menu(context, parent, calling_page=None):
    return {
        'calling_page': calling_page,
        'menuitems': menuitems_children(parent),
        'request': context['request'],
    }
