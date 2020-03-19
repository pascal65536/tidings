import os
import json
from django import template
from rssapp.models import BaseUrl

register = template.Library()
directory = '/tmp/news_project/'


@register.simple_tag
def get_sidebar_menu():
    """
    Работаем с json-файлом, содержащим боковое меню.
    Словарь для меню читаем из файла, если файла нет, то запрашиваем у БД, создаем словарь и сохраняем его в json.
    """
    sidebar_cache = 'sidebar_cache.json'
    file_cache = os.path.join(directory, sidebar_cache)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.isfile(file_cache):
        with open(file_cache, 'r') as f:
            return json.load(f)

    base_url_qs = BaseUrl.objects.all()
    base_url_lst = list()
    for base_url in base_url_qs:
        base_url_lst.append(
            {
                "id": str(base_url.id),
                "name": str(base_url.name),
                "url": str(base_url.url),
            })
    with open(file_cache, 'w') as f:
        json.dump(base_url_lst, f)
    return base_url_lst

