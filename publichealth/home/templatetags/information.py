# -*- coding: utf-8 -*-
from django import template
from django.utils import translation

from ..models.snippets import Contact, SocialContact

register = template.Library()

def get_contacts(the_site):
    if not the_site: return {}

    # Selected or default contact snippet
    top_contact = Contact.objects.filter(home_site=the_site)
    if top_contact.exists():
        top_contact = top_contact.first()
    else:
        default_contact = Contact.objects.filter(home_site=None)
        if default_contact.exists():
            top_contact = default_contact.first()
        else:
            top_contact = Contact.objects.first()

    # Selected or default social contact snippet
    social_contacts = SocialContact.objects.filter(home_site=the_site)
    if social_contacts.exists():
        social_contacts = social_contacts.all()
    else:
        default_contacts = SocialContact.objects.filter(home_site=None)
        if default_contacts.exists():
            social_contacts = default_contacts.all()
        else:
            social_contacts = SocialContact.objects.all()
    return {
        'contact': top_contact,
        'socials': social_contacts
    }

# Contact information (footer)
@register.inclusion_tag('tags/contact_info.html')
def contact_info(the_site):
    return get_contacts(the_site)

# Contact form (footer)
@register.inclusion_tag('tags/footer_form.html')
def footer_form(the_site):
    cc = get_contacts(the_site)
    if cc['contact']:
        return { 'form': cc['contact'].contact_form }
    return None

# Contact links (header)
@register.inclusion_tag('tags/contact_links.html')
def contact_links(the_site):
    return get_contacts(the_site)

# Styled contact name (header)
@register.inclusion_tag('tags/contact_name.html')
def contact_name(the_site, html=True):
    contactname = get_contacts(the_site)['contact']
    return { 'contact': contactname, 'html': html }
