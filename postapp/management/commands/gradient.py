from django.core.management import BaseCommand
from newsproject.utils import opengraph
from postapp.models import Post


class Command(BaseCommand):

    def handle(self, *args, **options):
        post_qs = Post.objects.filter(deleted=None).exclude(photo=None)
        for post_obj in post_qs:
            print(post_obj)
            Post.objects.filter(id=post_obj.id).update(og_picture=opengraph(post_obj))

