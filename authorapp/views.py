from __future__ import unicode_literals
from django.shortcuts import render
from authorapp.models import Author
from django.db.models import Q
from django.utils import timezone

from newsproject.settings_site import find_me, about_me, author_profile, author_title, author_list, sitename, \
    my_news_press


def author(request):
    author_set = Author.objects.filter(is_hide=False).order_by('order')[:18]
    context = {
        'title': '{} | {}'.format(author_title, sitename),
        'author_list': author_list,
        'menu_links': 'menu_links',
        'author_set': author_set
    }
    return render(request, 'authorapp/author.html', context)


def person(request, slug):
    query_set = ((Q(reporter__slug=slug) | Q(photographer__slug=slug)) & Q(date_start__lte=timezone.now()))
    author_page = Author.objects.get(slug=slug)
    news_author = News.objects.filter(query_set)[:12]
    news_author.aggregate()
    context = {
        'title': '{} | {}'.format(author_title, author_page.name),
        'author_profile': author_profile,
        'about_me': about_me,
        'find_me': find_me,
        'menu_links': 'menu_links',
        'author_page': author_page,
        'news_author': news_author,
        'my_news_press': my_news_press,
    }
    return render(request, 'authorapp/details.html', context)
