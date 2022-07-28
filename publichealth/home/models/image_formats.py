# image_formats.py
from django.utils.html import format_html
from wagtail.images.formats import Format, register_image_format


class OriginalImageFormat(Format):

    def image_to_html(self, image, alt_text, extra_attributes=None):

        default_html = super().image_to_html(image, alt_text, extra_attributes)

        return format_html("{}<figcaption>{}</figcaption>", default_html, alt_text)


register_image_format(
    OriginalImageFormat('original_fullwidth', 'Original image', 'bodytext-image', 'original')
)
