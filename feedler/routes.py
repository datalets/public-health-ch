# -*- coding: utf-8 -*-

from datetime import date

from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query

class FeedlerRoutes(RoutablePageMixin):

    @route(r'^$')
    def entries_list(self, request, *args, **kwargs):
        self.entries = self.get_entries()
        return Page.serve(self, request, *args, **kwargs)
