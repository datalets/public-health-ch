from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from wagtail.contrib.sitemaps.views import sitemap

from puput import urls as puput_urls
from feedler import urls as feedler_urls

from publichealth.search import views as search_views

urlpatterns = [
    url(r'', include(puput_urls)),
    url(r'', include(feedler_urls)),

    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),

    url('^sitemap\.xml$', sitemap),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Add views for testing 404 and 500 templates
    urlpatterns += [
        url(r'^test404/$', TemplateView.as_view(template_name='404.html')),
        url(r'^test500/$', TemplateView.as_view(template_name='500.html')),
    ]


urlpatterns += i18n_patterns(
    # These URLs will have /<language_code>/ appended to the beginning

    url(r'', include(wagtail_urls)),
)
