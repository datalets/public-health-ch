# -*- coding: utf-8 -*-

from wagtail.contrib.wagtailapi.endpoints import BaseAPIEndpoint
from wagtail.contrib.wagtailapi.serializers import BaseSerializer
from wagtail.contrib.wagtailapi.filters import FieldsFilter, OrderingFilter, SearchFilter
from wagtail.contrib.wagtailapi.pagination import WagtailPagination

from .models import Entry

class EntrySerializer(BaseSerializer):
    pass

class EntriesAPIEndpoint(BaseAPIEndpoint):
    base_serializer_class = EntrySerializer
    filter_backends = [FieldsFilter, OrderingFilter, SearchFilter]
    extra_api_fields = [
        'title',
        'author',
        'link',
        'visual',
        'content',
        'tags',
        'published',
    ]
    name = 'entries'
    model = Entry
