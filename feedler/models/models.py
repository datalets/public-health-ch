# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.views import IndexView
from django.utils import translation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField

class Stream(models.Model):
    title = models.CharField(max_length=255)
    ident = models.CharField(max_length=255)

    def __str__(self):
        return self.title

LANGUAGE_CHOICES = (
    ('de', 'Deutsch'),
    ('fr', 'Français'),
    ('it', 'Italiano'),
    ('en', 'English'),
    ('',   ' * * * '),
)

class Entry(models.Model):
    """Implementation of the Entry from the feedly API as generic Django model
    """
    raw = models.TextField(blank=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    published = models.DateTimeField(auto_now_add=True, editable=False)
    entry_id = models.CharField(max_length=255, unique=True, blank=True, editable=False)

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    link = models.URLField()
    visual = models.URLField(blank=True)
    lang = models.CharField(max_length=2, blank=True, default='', choices=LANGUAGE_CHOICES)
    content = models.TextField()
    tags = models.TextField(blank=True)

    stream = models.ForeignKey(Stream,
        blank=True, on_delete=models.CASCADE,
        verbose_name='Original stream')

    class Meta:
        verbose_name_plural = 'Entries'

class FeedPage(Page):
    intro = RichTextField(default='', blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.PROTECT,
        null=True, blank=True, verbose_name='Filter to stream (optional)')

    content_panels = [
        FieldPanel('title'),
        FieldPanel('intro'),
        FieldPanel('stream'),
    ]

    @property
    def feedentries(self):
        if self.stream:
            entries = Entry.objects.filter(stream=self.stream)
        else:
            entries = Entry.objects.all()
        # Filter out by chosen language
        curlang = translation.get_language()
        if curlang in ['de']:
            entries = entries.exclude(lang='fr')
        elif curlang in ['fr']:
            entries = entries.exclude(lang='de')
        # Order by most recent date first
        return entries.order_by('-published')[:72]

    def get_context(self, request):
        # Update template context
        context = super(FeedPage, self).get_context(request)

        # Wrap with pagination
        paginator = Paginator(self.feedentries, 9)
        page = request.GET.get('page')
        try:
            feedentries = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            feedentries = paginator.page(1)

        context['feedentries'] = feedentries
        return context

    class Meta:
        verbose_name = "Feeds"
