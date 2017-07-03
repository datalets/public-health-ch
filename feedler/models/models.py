# -*- coding: utf-8 -*-

from datetime import datetime

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

    def parse(self, raw, stream):
        """
        Parse the raw JSON implementation from the Feedly API
        """
        self.raw = raw
        self.stream = stream

        ts = raw['published'] / 1000
        self.published = datetime.utcfromtimestamp(ts)
        self.entry_id = raw['id']

        self.title = raw['title']

        if 'author' in raw['origin']:
            self.author = raw['author']
        elif 'title' in raw['origin']:
            self.author = raw['origin']['title']

        if len(raw['alternate']) > 0:
            self.link = raw['alternate'][0]['href']
        if 'visual' in raw and 'url' in raw['visual']:
            self.visual = raw['visual']['url']

        self._buildContent()

    def _buildContent(self):
        # Collect text content
        if 'content' in self.raw:
            self.content = self.raw['content']
        else:
            if 'summary' in self.raw:
                if 'content' in self.raw['summary']:
                    self.content = self.raw['summary']['content']
                else:
                    self.content = self.raw['summary']
            else:
                self.content = ''
        # Collect tags
        tags = []
        for tag in self.raw['tags']:
            if 'label' in tag:
                label = tag['label'].replace(',','-')
                label = label.strip().lower()
                if len(label) > 3 and not label in tags:
                    tags.append(label)
        self.tags = ','.join(tags)

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
