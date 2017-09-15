# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils import translation
from django.conf import settings

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.blocks import StructBlock, CharBlock, URLBlock, RichTextBlock, ListBlock, TextBlock, ChoiceBlock
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from puput.models import EntryPage, BlogPage
from feedler.models import Entry, Stream
from itertools import chain

from ..util import TranslatedField

class InfoBlock(StructBlock):
    title = CharBlock(required=True)
    photo = ImageChooserBlock(required=True)
    summary = RichTextBlock(required=True)
    action = CharBlock(required=False)
    url = URLBlock(required=False)

class ArticleIndexPage(Page):
    title_fr = models.CharField(max_length=255, default="")
    trans_title = TranslatedField(
        'title',
        'title_fr',
    )

    intro_de = RichTextField(default='', blank=True)
    intro_fr = RichTextField(default='', blank=True)
    trans_intro = TranslatedField(
        'intro_de',
        'intro_fr',
    )

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro_de'),
        FieldPanel('title_fr'),
        FieldPanel('intro_fr'),
        ImageChooserPanel('feed_image'),
    ]

    def get_context(self, request):
        context = super(ArticleIndexPage, self).get_context(request)
        articles = ArticlePage.objects.child_of(self).live()
        context['articles'] = articles
        subcategories = ArticleIndexPage.objects.child_of(self).live()
        context['subcategories'] = subcategories
        return context

    parent_page_types = [
        'home.ArticleIndexPage',
        'home.HomePage'
    ]
    subpage_types = [
        'home.ArticlePage',
        'home.ArticleIndexPage',
        'home.ContactForm',
        'wagtailcore.Page'
    ]
    class Meta:
        verbose_name = "Rubrik"

class ImageCarouselBlock(StructBlock):
    image = ImageChooserBlock()
    caption = TextBlock(required=False)

    class Meta:
        icon = 'image'

class ArticlePage(Page):
    title_fr = models.CharField(max_length=255, default="")
    trans_title = TranslatedField(
        'title',
        'title_fr',
    )

    intro_de = RichTextField(default='', blank=True)
    intro_fr = RichTextField(default='', blank=True)
    trans_intro = TranslatedField(
        'intro_de',
        'intro_fr',
    )

    gallery = StreamField([
        ('image', ListBlock(ImageCarouselBlock(), icon="image")),
    ], blank=True)
    # documents = StreamField([
    #     ('documents', ListBlock(DocumentChooserBlock(), icon="document")),
    # ])

    body_de = StreamField([
        ('paragraph', RichTextBlock()),
        ('section', CharBlock(classname="full title")),
        ('info', InfoBlock(icon='help')),
        ('media', ChoiceBlock(choices=[
            ('gallery', 'Image gallery'),
        ], icon='media'))
    ], null=True, blank=True)
    body_fr = StreamField([
        ('paragraph', RichTextBlock()),
        ('section', CharBlock(classname="full title")),
        ('info', InfoBlock(icon='help')),
        ('media', ChoiceBlock(choices=[
            ('gallery', 'Image gallery'),
        ], icon='media'))
    ], null=True, blank=True)
    trans_body = TranslatedField(
        'body_de',
        'body_fr',
    )

    date = models.DateField("Date", null=True, blank=True)

    on_homepage = models.BooleanField(default=False, verbose_name="Featured",
        help_text="Auf der Frontpage anzeigen")

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('title',    partial_match=True, boost=10),
        index.SearchField('title_fr', partial_match=True, boost=10),
        index.SearchField('body_de',  partial_match=True),
        index.SearchField('body_fr',  partial_match=True),
        index.SearchField('intro_de', partial_match=True),
        index.SearchField('intro_fr', partial_match=True),
    ]
    content_panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('intro_de'),
        ], heading="Deutsch"),
        StreamFieldPanel('body_de'),
        MultiFieldPanel([
            FieldPanel('title_fr'),
            FieldPanel('intro_fr'),
        ], heading="Français"),
        StreamFieldPanel('body_fr'),
        MultiFieldPanel([
            ImageChooserPanel('feed_image'),
        ], heading="Images"),
        StreamFieldPanel('gallery'),
    ]
    promote_panels = [
        InlinePanel('related_links', label="Links"),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('on_homepage'),
        ], heading="Veröffentlichung"),
        MultiFieldPanel(Page.promote_panels, "Einstellungen"),
    ]

    parent_page_types = [
        'home.ArticleIndexPage',
        'home.HomePage'
    ]
    subpage_types = []
    class Meta:
        verbose_name = "Artikel"

class ArticleRelatedLink(Orderable):
    page = ParentalKey(ArticlePage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()
    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]

class HomePage(Page):
    intro_de = RichTextField(default='')
    intro_fr = RichTextField(default='')
    trans_intro = TranslatedField(
        'intro_de',
        'intro_fr',
    )

    body_de = RichTextField(default='', blank=True)
    body_fr = RichTextField(default='', blank=True)
    trans_body = TranslatedField(
        'body_de',
        'body_fr',
    )

    infos_de = StreamField([
        ('info', InfoBlock())
    ], null=True, blank=True)
    infos_fr = StreamField([
        ('info', InfoBlock())
    ], null=True, blank=True)
    trans_infos = TranslatedField(
        'infos_de',
        'infos_fr',
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro_de', classname="full"),
            FieldPanel('body_de', classname="full"),
            StreamFieldPanel('infos_de'),
        ], heading="Deutsch"),
        MultiFieldPanel([
            FieldPanel('intro_fr', classname="full"),
            FieldPanel('body_fr', classname="full"),
            StreamFieldPanel('infos_fr'),
        ], heading="Français"),
    ]

    @property
    def featured(self):
        # Get list of live pages that are descendants of this page
        articles = ArticlePage.objects.live() #.descendant_of(self)
        articles = articles.filter(on_homepage=True)
        # Order by most recent date first
        #articles = articles.order_by('-date')
        return articles[:4]

    @property
    def blogentries(self):
        # Get list of latest news
        curlang = translation.get_language()
        if not curlang in ['de', 'fr']: curlang = 'de' # Default language
        parent = BlogPage.objects.filter(slug='news-%s' % curlang)
        if not parent: return []
        posts = EntryPage.objects.live().descendant_of(parent[0])
        # Order by most recent date first
        posts = posts.order_by('-date')
        return posts[:settings.BLOG_ENTRIES_HOME_PAGE]

    @property
    def newsentries(self):
        # Get the last few news entries for the home page
        entries = Entry.objects.all().order_by('-published')
        # Filter out by current language
        curlang = translation.get_language()
        if curlang in ['de']:
            entries = entries.exclude(lang='fr')
        elif curlang in ['fr']:
            entries = entries.exclude(lang='de')
        news = events = jobs = []
        Stream1 = Stream.objects.filter(title='News')
        if Stream1: news = entries.filter(stream=Stream1)
        Stream2 = Stream.objects.filter(title='Events')
        if Stream2: events = entries.filter(stream=Stream2)
        Stream3 = Stream.objects.filter(title='Jobs')
        if Stream3: jobs = entries.filter(stream=Stream3)
        i = settings.NEWS_ENTRIES_HOME_PAGE
        return list(chain(news[:i], events[:i], jobs[:i]))

    def get_context(self, request):
        # Update template context
        context = super(HomePage, self).get_context(request)
        context['featured'] = self.featured
        context['blogentries'] = self.blogentries
        context['newsentries'] = self.newsentries
        context['entryfeeds'] = settings.STREAMS_ON_HOME_PAGE
        return context

    parent_page_types = ['wagtailcore.Page']
    class Meta:
        verbose_name = "Frontpage"
