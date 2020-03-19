import requests
from django.core.management import BaseCommand
from lxml.html.clean import Cleaner

from rssapp.models import Content

cleaner = Cleaner(style=True, links=True, add_nofollow=True, page_structure=False, safe_attrs_only=False)


def clear_text(string):
    """
    Очистим это
    """
    string = string.replace('\n', ' ')
    string = string.replace('\t', ' ')
    string = string.replace('  ', ' ')
    return string


def get_translate(text):
    """
    Переведем это
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?lang=en-ru&key={}&text={}'.format(TRANSLATE_KEY, text)
    req = requests.get(url)
    req.encoding = 'utf-8'
    result_dct = req.json()
    print(len(text))
    return result_dct.get('text')[0]


class Command(BaseCommand):
    def handle(self, *args, **options):

        content_qs = Content.objects.filter(tr_title=None)
        for content in content_qs:
            if not content.title:
                continue
            tr_title = get_translate(clear_text(content.title))
            cnt = Content.objects.filter(id=content.id)
            cnt.update(tr_title=tr_title)

        content_qs = Content.objects.filter(tr_lead=None)
        for content in content_qs:
            if not content.lead:
                continue
            tr_lead = get_translate(clear_text(content.lead))
            cnt = Content.objects.filter(id=content.id)
            cnt.update(tr_lead=tr_lead)

        content_qs = Content.objects.filter(tr_text=None)
        for content in content_qs:
            if not content.text:
                continue
            tr_text = get_translate(clear_text(content.text))
            cnt = Content.objects.filter(id=content.id)
            cnt.update(tr_text=tr_text)
