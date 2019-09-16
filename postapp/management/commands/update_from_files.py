import datetime
import os
import uuid
from django.core.management import BaseCommand

from postapp.models import Post


def convert_rtf(file_name):

    name = uuid.uuid4()
    os.system("abiword --to=txt --to-name=/tmp/%s.txt  '%s'" % (name, file_name))
    tmp_name = '/tmp/%s.txt' % name

    with open(tmp_name, 'r') as file:
        plain_list = []
        for line in file:
            plain_list.append(line.strip())
    ret = ''
    title = ''
    lead = ''

    for pl in plain_list:
        alpha = 0
        digit = 0
        clean_pl = pl.replace('\u202d', '').replace('\u202c', '')
        for p in clean_pl:
            if p.isalpha():
                alpha += 1
            if p.isdigit():
                digit += 1

        if 'file:///home/pascal65536/Yandex.Disk/txt_rtf/' in clean_pl:
            continue
        elif 'Евлалия' in clean_pl:
            continue
        elif 'убрика' in clean_pl:
            continue
        elif 'РУБРИКА' in clean_pl:
            continue
        elif 'ИНФОРМАЦ' in clean_pl:
            continue
        elif 'вводка' in clean_pl:
            continue
        elif 'врезка' in clean_pl:
            continue
        elif alpha < digit:
            continue
        elif clean_pl[-1:] in ['.', ',', '!', '?', '"', ';']:
            ret += '<p>%s</p>' % clean_pl
            if not lead:
                lead = clean_pl
        elif not title:
            if not len(clean_pl) == 0 and len(clean_pl) < 255:
                title = clean_pl
        elif len(clean_pl) == 0:
            continue
        else:
            ret += '<p><b>%s</b></p>' % clean_pl

    # import ipdb; ipdb.set_trace()
    return title, lead, ret


class Command(BaseCommand):
    def handle(self, *args, **options):

        tree = os.walk('/home/pascal65536/Yandex.Disk/txt_rtf')
        count = 0
        # Рекурсивно перебрать каталог с текстами
        escape = ['', 'home', 'pascal65536', 'Yandex.Disk', 'txt_rtf', 'rtf', 'rtf~']

        for tr in tree:
            if tr[-1:][0]:
                for txt in tr[-1:][0]:
                    if '~' in txt:
                        continue
                    pth = []
                    pth += tr[0].split('/')
                    pth += txt.split('.')

                    for esc in escape:
                        if esc in pth:
                            pth.remove(esc)
                    path = '%s/%s' % (tr[0], txt)
                    print(path)
                    print('=' * 80)

                    # import ipdb; ipdb.set_trace()

                    title, lead, html = convert_rtf(path)

                    if len(title) == 0:
                        title = txt.split('.')[0]

                    if len(title) == 0 or len(lead) == 0:
                        import ipdb; ipdb.set_trace()

                    os.rename(path, path + '~')

                    post = Post()
                    post.charter_id = 1
                    post.title = title
                    post.text = html
                    post.date_post = datetime.datetime.now()
                    post.deleted = datetime.datetime.now()
                    post.lead = lead
                    post.save()

                    for tags in pth:
                        post.tags.add(tags)
                    print(pth)
                    print(title)
                    print(lead)
                    print('-' * 80)

                    # import ipdb; ipdb.set_trace()
                    count += 1

        print(count)
