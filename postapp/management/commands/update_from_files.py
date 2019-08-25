from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):

        import ipdb; ipdb.set_trace()

        file_name = '/home/pascal65536/Загрузки/нюанс.rtf'
        with open(file_name, 'r') as file:
            for rtf in file:
                print(rtf)

        # tree = os.walk('/home/pascal65536/Yandex.Disk/txt_rtf')
        # for tr in tree:
        #     # len(tr[len(tr)-1])
        #     print(tr)
