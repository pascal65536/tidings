import os
import re
import textwrap
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from django.utils import timezone
import uuid
from postapp.management.commands.feed import get_clean_text


def get_filename(filename, request):
    return filename.upper()


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


def latin_filename(instance, filename):
    date_post = timezone.now()
    f_folder = os.path.join('{:%Y/%m/%d}'.format(date_post))
    salt = '{:%M%S}'.format(date_post)
    part_of_name = filename.split(".")
    f_name = cyr_lat(instance.title)
    f_ext = cyr_lat(part_of_name[-1])
    return format('{}/{}/{}_{}.{}'.format('blog_picture', f_folder, f_name, salt, f_ext))


def old_opengraph(instance):
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
    date_post = timezone.now()
    salt = '{:%Y/%m/%d}'.format(date_post)
    directory = os.path.join(settings.MEDIA_ROOT, 'opengraph', 'post', salt)
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = '{}.{}'.format(uuid.uuid4(), 'png')
    image.save('{}/{}'.format(directory, filename))
    return format('{}/{}/{}/{}'.format('opengraph', 'post', salt, filename))


def opengraph(post_obj):

    # Возьмем картинку из БД
    photo_obj = post_obj.photo

    font_size = 36
    pic_width = 1024
    pic_height = 512
    max_color = (255, 255, 255)

    fill_image = Image.new("RGB", (pic_width, pic_height), max_color)
    if photo_obj and os.path.exists(photo_obj.picture.path):
        input_im = Image.open(str(photo_obj.picture.path))
        if input_im.mode != 'RGBA':
            input_im = input_im.convert('RGBA')

        # Найдём цвет для градиента
        unique_colors = dict()
        for i in range(input_im.size[0]):
            for j in range(input_im.size[1]):
                pixel = input_im.getpixel((i, j))
                unique_colors.setdefault(pixel, 0)
                unique_colors[pixel] += 1
        max_color = (0, 0, 0)
        max_color_count = 0
        for k, v in unique_colors.items():
            if v > max_color_count and len(set(list(k)[0:3])) > 1:
                max_color_count = v
                max_color = k

        # Это картинка для соцсетей
        (w, h) = input_im.size
        if w / h < pic_width / pic_height:
            percent = pic_width / w
        else:
            percent = pic_height / h
        width = int(w * percent)
        height = int(h * percent)
        input_im = input_im.resize((width, height), Image.ANTIALIAS)
        yc = int((height - pic_height) / 2)
        xc = 0
        input_im = input_im.crop((xc, yc, xc + pic_width, yc + pic_height))

        alpha_gradient = Image.new('L', (pic_width, 1), color=0)
        for x in range(pic_width):
            a = int((1 * 255.) * (1. - 0.7 * float(x) / pic_width))
            if a > 0:
                alpha_gradient.putpixel((x, 0), a)
            else:
                alpha_gradient.putpixel((x, 0), 0)

        alpha = alpha_gradient.resize(input_im.size)

        # create black image, apply gradient
        black_im = Image.new('RGBA', (pic_width, pic_height), color=max_color)
        black_im.putalpha(alpha)

        # make composite with original image
        fill_image = Image.alpha_composite(input_im, black_im)

    if min(max_color) > 127:
        font_color = (0, 0, 0)
    else:
        font_color = (255, 255, 255)

    text = post_obj.title
    unicode_text = "\n".join(textwrap.wrap(text, width=30))
    draw = ImageDraw.Draw(fill_image)
    unicode_font = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, 'fonts', 'Oswald-Medium.ttf'), font_size)
    text_width, text_height = draw.textsize(unicode_text, font=unicode_font)
    text_top = (pic_height - text_height) // 2
    text_left = (pic_width - text_width) // 2
    draw.text((text_left, text_top), unicode_text, font=unicode_font, fill=font_color)

    # Создадим путь и имя файла
    date_post = timezone.now()
    salt = '{:%Y/%m/%d}'.format(date_post)
    directory = os.path.join(settings.MEDIA_ROOT, 'opengraph', 'post', salt)
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = '{}.{}'.format(uuid.uuid4(), 'png')
    fill_image.save('{}/{}'.format(directory, filename), format='PNG', dpi=[72, 72])
    return format('{}/{}/{}/{}'.format('opengraph', 'post', salt, filename))


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
    if not os.path.exists('dictionary'):
        os.makedirs('dictionary')
    tags_lst = list()
    plain_list = set()
    with open('dictionary/word_rus.txt', 'r') as fl:
        for line in fl:
            plain_list.add(line.strip().upper())
    alphabet = 'йцукенгшщзхъёфывапролджэячсмитьбю'
    backspase = ['    ', '   ', '  ']
    for post in post_qs:
        text = get_clean_text(post.text)
        new_text = ''
        for t in text:
            new_text += t if t in alphabet or t in alphabet.upper() else ' '

        for bs in backspase:
            new_text = new_text.replace(bs, ' ')

        tags = plain_list & set(new_text.upper().split(' '))

        for tag in tags:
            tags_lst.append(tag.capitalize())

    return tags_lst


def get_recent_for_tags(post, user):
    """
    Найдём похожие посты по тегам
    """
    from postapp.models import Post
    from collections import OrderedDict
    tags_set = set(post.tags.all().values_list('slug', flat=True))
    post_dct = dict()
    post_qs = Post.objects.for_user(user).exclude(id=post.id).filter(tags__slug__in=tags_set)
    for post in post_qs:
        post_dct.setdefault(post, 0)
        post_dct[post] += 1

    recent_for_tags = []
    post_dct_sorted_by_value = OrderedDict(sorted(post_dct.items(), key=lambda x: x[1], reverse=True))
    for kk, vv in post_dct_sorted_by_value.items():
        if vv > 3:
            recent_for_tags.append(kk.id)

    return recent_for_tags


def find_img(text):
    """
    Обработка текста. Будем искать картинку и вставлять класс.
    """
    img_lst = re.findall(r'<img[A-Za-z0-9 =\/\":._%;]*>', text)
    for img in img_lst:
        img_new = re.sub(r'style=\"[A-Za-z0-9 =\/:._%;]*\"', 'class="card-img"', img)
        text = text.replace(img, img_new)
    return text


def delete_tags(value):
    value = re.sub(r'(\<(/?[^>]+)>)', '', value)
    value = re.sub(r'&[a-z]*;', ' ', value)
    return value


def process_text(text):
    text = re.sub(r'(role|dir|allowfullscreen|frameborder|name|style|align|height|original_image|thumb_option|title|width|filer_id)="[% \w:,-;]*"', '', text)
    text = re.sub(r'&laquo;', '"', text)
    text = re.sub(r'&ldquo;', '"', text)
    text = re.sub(r'&raquo;', '"', text)
    text = re.sub(r'&rdquo;', '"', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&mdash;', '-', text)
    text = re.sub(r'&ndash;', '-', text)
    text = re.sub(r'&hellip;', '...', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&micro;', 'µ', text)
    text = re.sub(r' >', '>', text)
    text = re.sub(r'<[/]*span>', '', text)
    text = re.sub(r'[ ]+', ' ', text)
    return text

