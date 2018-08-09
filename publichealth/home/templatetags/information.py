# -*- coding: utf-8 -*-
from django import template
from django.utils import translation

from ..models.snippets import Contact, SocialContact

register = template.Library()

def get_contacts(site_root):
    if not site_root: return {}
    site = site_root.get_site()

    # Selected or default contact snippet
    top_contact = Contact.objects.filter(home_site=site)
    if top_contact.exists():
        top_contact = top_contact.last()
    else:
        default_contact = Contact.objects.filter(home_site=None)
        if default_contact.exists():
            top_contact = default_contact.last()
        else:
            top_contact = Contact.objects.last()

    # Selected or default social contact snippet
    social_contacts = SocialContact.objects.filter(home_site=site)
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
def contact_info(site_root):
    return get_contacts(site_root)

# Contact form (footer)
@register.inclusion_tag('tags/footer_form.html')
def footer_form(site_root):
    cc = get_contacts(site_root)
    if cc['contact']:
        return { 'form': cc['contact'].contact_form }
    return None

# Contact links (header)
@register.inclusion_tag('tags/contact_links.html')
def contact_links(site_root):
    return get_contacts(site_root)

# Styled contact name (header)
@register.inclusion_tag('tags/contact_name.html')
def contact_name(site_root, html=True):
    contactname = get_contacts(site_root)['contact']
    return { 'contact': contactname, 'html': html }
