from django.core.management import BaseCommand

from photoapp.models import Photo
from postapp.models import Post


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Заменить прямое вхождение картинки на ссылку на таблицу с картинками.
        :param args:
        :param options:
        :return:
        """
        post_qs = Post.objects.filter(photo=None).exclude(picture='')
        for post in post_qs:
            photo = Photo()
            photo.title = post.title
            photo.picture = post.picture
            photo.save()
            Post.objects.filter(id=post.id).update(photo=photo)
