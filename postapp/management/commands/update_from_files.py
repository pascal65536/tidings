from django.core.management import BaseCommand
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        tree = os.walk('/home/pascal65536/Yandex.Disk/txt prototype24/prototype24')
        for tr in tree:
            print(tr)
