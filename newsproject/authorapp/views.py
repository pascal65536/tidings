from __future__ import unicode_literals
from django.shortcuts import render
import contactapp.settings_site as site
from authorapp.models import Author

author_list = Author.objects.all().order_by('name')


def author(request):
    context = {
        'title': 'Авторы | {}'.format(site.sitename),
        'menu_links': 'menu_links',
        'author_list': author_list,
        'lnk': 'https://www.facebook.com/gornovosti.ru/',
    }
    return render(request, 'authorapp/author.html', context)
