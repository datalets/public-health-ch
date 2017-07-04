# -*- coding: utf-8 -*-

from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField

class Stream(models.Model):
    title = models.CharField(max_length=255)
    ident = models.CharField(max_length=255)

    def __str__(self):
        return self.title

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
        # Order by most recent date first
        entries = entries.order_by('-published')
        return entries[:10]

    def get_context(self, request):
        # Update template context
        context = super(FeedPage, self).get_context(request)
        context['feedentries'] = self.feedentries
        return context

    class Meta:
        verbose_name = "Feeds"
