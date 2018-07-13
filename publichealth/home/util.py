from django.utils import translation

class TranslatedField(object):
    def __init__(self, de_field, fr_field, en_field):
        self.de_field = de_field
        self.fr_field = fr_field
        self.en_field = en_field

    def __get__(self, instance, owner):
        if translation.get_language() == 'fr':
            val = getattr(instance, self.fr_field)
        elif translation.get_language() == 'en':
            val = getattr(instance, self.en_field)
        else:
            return getattr(instance, self.de_field)
        if not val:
            return getattr(instance, self.de_field)
        return val
