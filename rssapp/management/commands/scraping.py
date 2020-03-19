from django.core.management import BaseCommand
import requests
from lxml.html import fromstring
from lxml.html.clean import Cleaner

from rssapp.models import BaseUrl, Content

cleaner = Cleaner(style=True, links=True, add_nofollow=True, page_structure=False, safe_attrs_only=False)


def escape(bad):
    bad = bad.replace('\n\n\t\t', '\n')
    bad = bad.replace('\n\n', '\n')
    bad = bad.replace('\n\t\t', '\n')
    bad = bad.replace('\xa0', '\n')
    bad = bad.replace(
        '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\n')
    bad = bad.replace('&', '&amp;')
    bad = bad.replace("'", '&#39;')
    bad = bad.replace('"', '&quot;')
    good = bad
    return (good)


def parse_elem(elem):
    ITEM_PATH_DETAILS = '#mainbody'

    a = elem.cssselect('a')[0]
    url = a.get('href')
    title = a.text
    img = elem.cssselect('img')[0]
    pic = img.get('src')

    details = requests.get(url)
    details_html = details.content.decode('utf-8')
    details_doc = fromstring(details_html)

    details = details_doc.cssselect(ITEM_PATH_DETAILS)[0]
    text = cleaner.clean_html(details).text_content()

    news = {
        'url': url,
        'title': title,
        'text': text,
        'pic': pic,
    }
    return news


class Command(BaseCommand):
    def handle(self, *args, **options):
        URL = 'https://technabob.com/'
        ITEM_PATH = '.post .innerpost .storycontent'
        rq = requests.get(URL)
        list_html = rq.content.decode('utf-8')
        list_doc = fromstring(list_html)
        elem_technabob = list_doc.cssselect(ITEM_PATH)
        baseurl, _ = BaseUrl.objects.get_or_create(name=URL)
        for elem in elem_technabob:
            defaults = parse_elem(elem)
            url = defaults.pop('url')
            defaults.update(baseurl=baseurl)
            content, _ = Content.objects.update_or_create(url=url, defaults=defaults)

# https://www.techradar.com/how-to
# https://kotaku.com/
# https://www.tomshardware.com/
# https://gizmodo.com/
