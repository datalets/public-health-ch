# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf.urls import url
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from django.shortcuts import redirect

from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.views import IndexView
from wagtail.admin import messages

from feedler.models import Entry
from feedler.refresh import refresh_streams
from feedler.models.admin import FeedlySettings

class RefreshButtonHelper(ButtonHelper):
    """
    This helper constructs a refresh button
    """
    button_classnames = ['icon', 'icon-download']
    def refresh_button(self, classnames_add=None, classnames_exclude=None):
        if classnames_add is None: classnames_add = []
        if classnames_exclude is None: classnames_exclude = []
        classnames = self.button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        text = _('Sync {}'.format(self.verbose_name_plural.title()))
        return {
            'url': self.url_helper.get_action_url('refresh', query_params=self.request.GET),
            'label': text, 'classname': cn, 'title': text,
        }

class RefreshAdminURLHelper(AdminURLHelper):
    """
    This helper constructs the different urls, to overwrite the default behaviour
    and append the filters to the action.
    """
    non_object_specific_actions = ('create', 'choose_parent', 'index', 'refresh')
    def get_action_url(self, action, *args, **kwargs):
        query_params = kwargs.pop('query_params', None)
        url_name = self.get_action_url_name(action)
        if action in self.non_object_specific_actions:
            url = reverse(url_name)
        else:
            url = reverse(url_name, args=args, kwargs=kwargs)
        if query_params:
            url += '?{params}'.format(params=query_params.urlencode())
        return url
    def get_action_url_pattern(self, action):
        if action in self.non_object_specific_actions:
            return self._get_action_url_pattern(action)
        return self._get_object_specific_action_url_pattern(action)

class RefreshView(IndexView):
    """
    A Class Based View which will handle the button click
    """
    # def export_csv(self):
    #     data = self.queryset.all()
    #     response = ...
    #     return response
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if not refresh_streams(FeedlySettings.for_site(request.site)):
            messages.error(
                request, _('Sorry, could not refresh streams. Please try again in a few minutes, then contact support if the issue persists.'))
        return redirect('/admin/feedler/entry/')


class EntryModelAdminMixin(object):
    """
    A mixin to add to your model admin which hooks the different helpers, the view
    and register the new urls.
    """
    button_helper_class = RefreshButtonHelper
    url_helper_class = RefreshAdminURLHelper
    view_class = RefreshView

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls += (
            url(
                self.url_helper.get_action_url_pattern('refresh'),
                self.refresh_view,
                name=self.url_helper.get_action_url_name('refresh')
            ),
        )
        return urls

    def refresh_view(self, request):
        kwargs = {'model_admin': self}
        view_class = self.view_class
        return view_class.as_view(**kwargs)(request)
