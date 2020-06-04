import json
import os
import re
import textwrap
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from django.utils import timezone
import uuid
from rssapp.management.commands.feed import get_clean_text


cyr2lat = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ъ': 'y',
    'ы': 'y',
    'ь': "i",
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Е': 'E',
    'Ё': 'Yo',
    'Ж': 'Zh',
    'З': 'Z',
    'И': 'I',
    'Й': 'Y',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'H',
    'Ц': 'Ts',
    'Ч': 'Ch',
    'Ш': 'Sh',
    'Щ': 'Shch',
    'Ъ': 'Y',
    'Ы': 'Y',
    'Ь': "I",
    'Э': 'E',
    'Ю': 'Yu',
    'Я': 'Ya',
    '!': '_',
    "'": '_',
    ' ': '_',
    ',': '_',
    '+': '_',
    '.': '_',
    ':': '_',
    '-': '_',
    '%': '_',
    '&': '_',
    '*': '_',
    '?': '_',
    '@': '_',
    '$': '_',
    '^': '_',
    '(': '_',
    ')': '_',
    '{': '_',
    '}': '_',
    '[': '_',
    ']': '_',
    '/': '_',
}


def cyr_lat(cyrillic):
    global cyr2lat
    for i, j in cyr2lat.items():
        cyrillic = cyrillic.replace(i, j).lower()
        while cyrillic.count('__') > 1:
            cyrillic = cyrillic.replace('__', '_')
    return cyrillic


def delete_tags(value):
    value = re.sub(r'(\<(/?[^>]+)>)', '', value)
    value = re.sub(r'&[a-z]*;', ' ', value)
    return value


def latin_filename(instance, filename):
    date_post = timezone.now()
    f_folder = os.path.join('{:%Y/%m/%d}'.format(date_post))
    salt = '{:%M%S}'.format(date_post)
    part_of_name = filename.split(".")
    f_name = cyr_lat(instance.title)
    f_ext = cyr_lat(part_of_name[-1])
    return format('{}/{}/{}_{}.{}'.format('blog_picture', f_folder, f_name, salt, f_ext))


def opengraph(instance):
    font_size = 36
    height = 480
    width = 640
    background_color = (255, 255, 255)
    font_color = (0, 0, 0)
    text = instance.title
    unicode_text = "\n".join(textwrap.wrap(text, width=30))
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)
    unicode_font = ImageFont.truetype("DejaVuSans.ttf", font_size)

    text_width, text_height = draw.textsize(unicode_text, font=unicode_font)
    text_top = (height - text_height) // 2
    text_left = (width - text_width) // 2

    draw.text((text_left, text_top), unicode_text, font=unicode_font, fill=font_color)

    # Создадим путь и имя файла
    directory = os.path.join(settings.MEDIA_ROOT, 'opengraph', 'post')
    if not os.path.exists(directory):
        os.makedirs(directory)
    date_post = timezone.now()
    filename = '{}.{}'.format(uuid.uuid4(), 'png')
    image.save('{}/{}'.format(directory, filename))
    return filename


def save_file(obj):
    file_uid = str(uuid.uuid4())
    relative_paths = os.path.join(settings.MEDIA_URL, file_uid)

    file_obj = os.path.join(relative_paths, obj.name)

    if not os.path.exists(relative_paths):
        os.makedirs(relative_paths)

    obj.seek(0)
    with open(file_obj, 'wb') as open_file:
        bufsize = 1024 * 1024  # 1 Мб
        while True:
            buf = obj.read(bufsize)
            if not buf:
                break
            open_file.write(buf)

    file_name = ''
    return file_name


def get_tags(post_qs):
    tags_lst = list()
    plain_list = set()
    category_lst = dict()
    with open('dictionary/file_cache.json', 'w') as f:
        json.dump(category_lst, f)
    # with open('dictionary/word_rus.txt', 'r') as fl:
    #     for line in fl:
    #         plain_list.add(line.strip().upper())
    # alphabet = 'йцукенгшщзхъёфывапролджэячсмитьбю'
    # backspase = ['    ', '   ', '  ']
    # for post in post_qs:
    #     text = get_clean_text(post.text)
    #     new_text = ''
    #     for t in text:
    #         new_text += t if t in alphabet or t in alphabet.upper() else ' '
    #
    #     for bs in backspase:
    #         new_text = new_text.replace(bs, ' ')
    #
    #     tags = plain_list & set(new_text.upper().split(' '))
    #
    #     for tag in tags:
    #         tags_lst.append(tag.capitalize())

    return tags_lst
