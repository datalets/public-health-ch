# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models

class EntryCategory(models.Model):
    """A structure for sorting through entry models
    """
    label = models.CharField(max_length=255)
    feedly_id = models.CharField(max_length=200)

class Entry(models.Model):
    """Implementation of the Entry from the feedly API as generic Django model
    """
    raw = models.TextField(blank=True)

    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(auto_now_add=True)
    entry_id = models.IntegerField(blank=True)

    title = models.CharField(max_length=255)
    origin_title = models.CharField(max_length=255, blank=True)
    link = models.URLField()
    visual = models.URLField(blank=True)

    content = models.TextField()
    tags = models.TextField(blank=True)

    categories = models.ManyToManyField(EntryCategory, blank=True)

    class Meta:
        verbose_name_plural = 'Entries'

    def _buildInstance(self, raw):
        """
        Parse the raw JSON implementation from the Feedly API
        """
        self.raw = raw

        self.published = datetime.utcfromtimestamp(raw['published'])
        self.entry_id = raw['id']

        self.title = raw['title']
        self.origin_title = raw['origin']['title']
        self.link = raw['alternate'][0]['href']
        self.visual = raw['visual']['url']

        self._buildContent()

        # if 'categories' in raw:
        #     self.categories = raw['categories']
        # else:
        #     self.categories = []

    def _buildContent(self):
        # Collect text content
        if 'content' in self.raw:
            self.content = self.raw['content']
        else:
            if 'summary' in self.raw:
                self.content = self.raw['summary']
            else:
                self.content = ''
        # Collect tags
        tags = []
        for tag in self.raw['tags']:
            if 'label' in tag:
                tags.push(tag['label'].replace(',','-'))
        self.tags = ','.join('tags')
