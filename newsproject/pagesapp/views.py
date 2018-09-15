from __future__ import unicode_literals
from django.shortcuts import render
import pagesapp.settings_site as site
from pagesapp.models import Contacts

contacts_list = Contacts.objects.all().order_by('name')


def contacts(request):
    context = {
        'title': 'Контакты | {}'.format(site.sitename),
        'menu_links': 'menu_links',
        'contacts_list': contacts_list
    }
    return render(request, 'pagesapp/contacts.html', context)
