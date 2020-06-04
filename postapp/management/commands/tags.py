import re

import html2text
from django.core.management import BaseCommand
from postapp.models import Post
from rssapp.management.commands.feed import get_clean_text


def dehtmlify(body):
    """
    HTML в MarkDown внезапно
    """
    html = html2text.HTML2Text()
    html.body_width = 0

    try:
        body = html.handle(body.replace("\r\n", "<br/>"))
        body = re.sub(r"^(\s*\n){2,}", "\n", body, flags=re.MULTILINE)
    except:
        pass
    return body


class Command(BaseCommand):

    def handle(self, *args, **options):

        plain_list = set()
        with open('dictionary/word_rus.txt', 'r') as fl:
            for line in fl:
                plain_list.add(line.strip().upper())
        alphabet = 'йцукенгшщзхъёфывапролджэячсмитьбю'
        backspase = ['    ', '   ', '  ']
        post_qs = Post.objects.all().order_by('-id')
        # post_qs = Post.objects.all().exclude(
        #     title__startswith='.').exclude(deleted=None)[0:1]
        for post in post_qs:
            text = get_clean_text(post.text)
            new_text = ''
            for t in text:
                new_text += t if t in alphabet or t in alphabet.upper() else ' '

            for bs in backspase:
                new_text = new_text.replace(bs, ' ')

            tags = plain_list & set(new_text.upper().split(' '))

            for tag in tags:
                post.tags.add(tag.capitalize())

            print(post.id, tags)



