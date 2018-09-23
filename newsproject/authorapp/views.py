from __future__ import unicode_literals
from django.shortcuts import render
import contactapp.settings_site as site
from authorapp.models import Author
from newsapp.models import News
import datetime
from django.db.models import Q


def author(request):
    author_set = Author.objects.all().order_by('name')
    context = {
        'title': '{} | {}'.format(site.author_title, site.sitename),
        'author_list': site.author_list,
        'menu_links': 'menu_links',
        'author_set': author_set
    }
    return render(request, 'authorapp/author.html', context)


def person(request, nickname):
    query_set = ((Q(reporter__nickname=nickname) | Q(photographer__nickname=nickname)) & Q(date_start__lte=datetime.datetime.now()))
    author_page = Author.objects.get(nickname=nickname)
    news_author = News.objects.filter(query_set)[:12]
    news_author.aggregate()
    context = {
        'title': '{} | {}'.format(site.author_title, author_page.name),
        'author_profile': site.author_profile,
        'about_me': site.about_me,
        'find_me': site.find_me,
        'menu_links': 'menu_links',
        'author_page': author_page,
        'news_author': news_author,
        'my_news_press': site.my_news_press,
    }
    return render(request, 'authorapp/details.html', context)
