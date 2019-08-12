# -*- coding: utf-8 -*-

from wagtail.api.v2.endpoints import BaseAPIEndpoint
from wagtail.api.v2.serializers import BaseSerializer
from wagtail.api.v2.filters import FieldsFilter, OrderingFilter, SearchFilter
from wagtail.api.v2.pagination import WagtailPagination

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
