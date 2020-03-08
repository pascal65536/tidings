import requests
from django.core.management import BaseCommand
from newsproject import settings
from postapp.models import Post


class Command(BaseCommand):

    def handle(self, *args, **options):
        post_qs = Post.objects.all().exclude(
            title__startswith='.').exclude(deleted=None)
        post = post_qs[111]
        text = post.text
        url = 'https://content-watch.ru/public/api/'

        data = {
            'action': 'CHECK_TEXT',
            'key': settings.API_KEY,
            'test': 0,
            'text': text
        }
        req = requests.post(url, data=data)
        req.encoding = 'utf-8'
        result_dct = req.json()
        print(post.id)
        print(post.title)
        print(result_dct.get('percent'))




