from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client

from wagtail.core.models import Page
from wagtail.admin.views.pages import edit

# Scans for broken editors, via
# https://github.com/wagtail/wagtail/issues/4602

class Command(BaseCommand):

    def handle(self, **options):
        invalid_page_ids = []
        pages = Page.objects.all()
        client = Client()
        # use any existing super user account
        user = User.objects.get(username='oleg')
        client.force_login(user)

        for page in pages:
            id = page.id
            # print statement to assure the script is running
            print(id)
            url = f'/cms/pages/{id}/edit/'
            try:
                response = client.get(url)
            except:
                invalid_pages.append(id)

        print(invalid_page_ids)
