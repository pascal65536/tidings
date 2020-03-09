import json

from django.core.management import BaseCommand

from roadmap.models import Distance


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(file, "r") as read_file:
            data_lst = json.load(read_file)

        city_dct = dict()
        for data in data_lst:
            src = data['fields']['src'].upper()
            src = src.replace('Ё', 'Е')
            dst = data['fields']['dst'].upper()
            dst = dst.replace('Ё', 'Е')
            distance = data['fields']['distance']
            city_dct.setdefault(src, {}).setdefault(dst, distance)

        # print (sorted(city_dct.keys()))

        for city in sorted(city_dct.keys()):
            for cd in city_dct[city]:
                print (city, cd, city_dct[city][cd])

                obj, new = Distance.objects.get_or_create(
                    src=city, dst=cd, distance=city_dct[city][cd]
                )
