# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _

from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.views import IndexView

from feedler.models import Entry

class ExportButtonHelper(ButtonHelper):
    """
    This helper constructs all the necessary attributes to create a button.

    There is a lot of boilerplate just for the classnames to be right :(
    """

    export_button_classnames = ['icon', 'icon-download']

    def export_button(self, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []

        classnames = self.export_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        text = _('Export {}'.format(self.verbose_name_plural.title()))

        return {
            'url': self.url_helper.get_action_url('export', query_params=self.request.GET),
            'label': text,
            'classname': cn,
            'title': text,
        }


class ExportAdminURLHelper(AdminURLHelper):
    """
    This helper constructs the different urls.

    This is mostly just to overwrite the default behaviour
    which consider any action other than 'create', 'choose_parent' and 'index'
    as `object specific` and will try to add the object PK to the url
    which is not what we want for the `export` option.

    In addition, it appends the filters to the action.
    """

    non_object_specific_actions = ('create', 'choose_parent', 'index', 'export')

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


class ExportView(IndexView):
    """
    A Class Based View which will generate
    """

    def export_csv(self):
        data = self.queryset.all()
        response = ...
        return response


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        return self.export_csv()


class ExportModelAdminMixin(object):
    """
    A mixin to add to your model admin which hooks the different helpers, the view
    and register the new urls.
    """

    button_helper_class = ExportButtonHelper
    url_helper_class = ExportAdminURLHelper

    export_view_class = ExportView

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls += (
            url(
                self.url_helper.get_action_url_pattern('export'),
                self.export_view,
                name=self.url_helper.get_action_url_name('export')
            ),
        )

        return urls

    def export_view(self, request):
        kwargs = {'model_admin': self}
        view_class = self.export_view_class
        return view_class.as_view(**kwargs)(request)


class MenuModelAdmin(ExportModelAdminMixin, ModelAdmin):
    model = Entry
