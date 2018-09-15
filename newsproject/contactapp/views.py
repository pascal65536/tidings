from __future__ import unicode_literals
from django.shortcuts import render
import contactapp.settings_site as site
from contactapp.models import Contact

contact_list = Contact.objects.all().order_by('name')


def contact(request):
    context = {
        'title': 'Контакты | {}'.format(site.sitename),
        'menu_links': 'menu_links',
        'contact_list': contact_list
    }
    return render(request, 'contactapp/contact.html', context)
