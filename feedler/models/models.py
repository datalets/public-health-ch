# -*- coding: utf-8 -*-

from django.db import models
from django.utils import translation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField

class Stream(models.Model):
    title = models.CharField(max_length=255)
    ident = models.CharField(max_length=255,
        help_text='Example: enterprise/myuser/tag/abcd...')

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
    entry_id = models.CharField(max_length=255, blank=True, editable=False)

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    link = models.URLField(max_length=500)
    visual = models.URLField(max_length=500, blank=True)
    lang = models.CharField(max_length=2, blank=True, default='', choices=LANGUAGE_CHOICES)
    content = models.TextField()
    tags = models.TextField(blank=True)

    stream = models.ForeignKey(Stream,
        blank=False, on_delete=models.CASCADE,
        verbose_name='Original stream')

    @property
    def with_image(self):
        if not self.visual: return u''
        return u'✔'

    class Meta:
        verbose_name_plural = 'Entries'
    def __str__(self):
        return self.title

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
