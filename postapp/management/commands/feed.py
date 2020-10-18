import re
import maya
import datetime
import html2text
import feedparser
from django.core.management import BaseCommand
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup

cleaner = Cleaner(style=True, links=True, add_nofollow=True, page_structure=False, safe_attrs_only=False)


def get_clean_text(details):
    """
    Очистим html от тегов
    """
    soup = BeautifulSoup(details, features="lxml")
    return soup.get_text().strip()


def get_pic(text):
    if 'img' not in text:
        return None
    for txt in text.split('<'):
        if not 'img' == txt[0:3]:
            continue
        for number, tx in enumerate(txt.split('"')):
            if 'src' in tx:
                return txt.split('"')[number+1]


class Command(BaseCommand):
    def handle(self, *args, **options):
        feed_lst = [
            'https://www.sparkfun.com/feeds/news',
            'https://hackaday.com/blog/feed/',
            'https://www.open-electronics.org/feed/rss/',
            'https://feeds2.feedburner.com/EmbeddedProjectsFromAroundTheWeb',
            'https://blog.adafruit.com/feed/',
            'https://blog.arduino.cc/feed/',
            'https://www.techradar.com/rss',
            'https://technabob.com/blog/feed',
            'https://kotaku.com/rss',
            'https://www.tomshardware.com/feeds/all',
            'https://gizmodo.com/rss',
            'https://lifehacker.com/rss',
            'https://krebsonsecurity.com/rss',
            'https://thewirecutter.com/rss',
            'https://www.schneier.com/blog/atom.xml',
            'https://www.technologyreview.com/rss/'
        ]
        for feed in feed_lst:
            rss = feedparser.parse(feed)
            defaults = {
                'name': rss['feed'].get('title'),
                'url': rss['feed'].get('link'),
            }

            baseurl, _ = BaseUrl.objects.update_or_create(feed=feed, defaults=defaults)

            for entry in rss['entries']:
                url = entry['link']
                text = ''
                if not text and 'content' in entry.keys():
                    text = cleaner.clean_html(entry['content'][0]['value'])
                if not text and 'summary_detail' in entry.keys():
                    text = cleaner.clean_html(entry['summary_detail']['value'])

                bad_lead = cleaner.clean_html(entry.get('summary'))
                pic = get_pic(bad_lead)
                if not pic:
                    pic = get_pic(text)
                lead = get_clean_text(bad_lead)

                published = datetime.datetime.now()
                if 'published' in entry.keys():
                    published = maya.parse(entry['published']).datetime()

                defaults = {
                    'title': entry.get('title'),
                    'lead': lead,
                    'baseurl': baseurl,
                    'text': text,
                    'pic': pic,
                    'published': published,
                }

                if not defaults['title']:
                    continue

                content, _ = Content.objects.update_or_create(url=url, defaults=defaults)




