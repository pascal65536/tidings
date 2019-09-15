import os
import uuid
import textwrap
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import TextField
from django.db.models.functions import datetime
from PIL import Image, ImageDraw, ImageFont
from taggit.managers import TaggableManager
from newsproject.utils import cyr_lat
from newsproject.settings import MEDIA_ROOT


def latin_filename(instance, filename):
    date_post = datetime.datetime.now()
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
    f_folder = os.path.join(MEDIA_ROOT, 'opengraph', 'post')
    date_post = datetime.datetime.now()
    salt = '{:%M%S}'.format(date_post)
    # f_name = str(instance.id)
    # f_name = utils.cyr_lat(instance.title)
    f_name = uuid.uuid4()
    f_ext = 'png'
    filename = '{}.{}'.format(f_name, f_ext)
    image.save('{}/{}'.format(f_folder, filename))
    return filename


class Charter(models.Model):
    title = models.CharField(verbose_name='Название', max_length=20)
    lead = TextField(verbose_name='Лидер-абзац', )
    order = models.IntegerField(verbose_name='Сортировка', default=1)
    slug = AutoSlugField(populate_from='title')
    text = RichTextField(verbose_name='Описание раздела', blank=True, null=True)
    picture = models.ImageField(verbose_name='Картинка раздела', upload_to=latin_filename, blank=True)
    og_picture = models.CharField(verbose_name='Картинка для соцсетей', max_length=255, blank=True)
    meta_title = models.CharField(max_length=255, verbose_name=u'Title', null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, verbose_name=u'Keywords', null=True, blank=True)
    meta_description = models.TextField(max_length=255, verbose_name=u'Description', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.og_picture = opengraph(self)
        super(Charter, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Название раздела'
        verbose_name_plural = 'Названия разделов'
        ordering = ['-order']

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(verbose_name='Заголовок поста', max_length=255)
    lead = models.TextField(verbose_name='Лидер-абзац', blank=True, null=True)
    text = RichTextField(verbose_name='Тело поста')
    charter = models.ForeignKey(Charter, blank=True, null=True, verbose_name='Раздел', on_delete=models.SET_NULL)
    date_post = models.DateTimeField(verbose_name='Дата начала публикации')
    picture = models.ImageField(verbose_name='Картинка для привлечения внимания', upload_to=latin_filename, blank=True)
    og_picture = models.CharField(verbose_name='Картинка для соцсетей', max_length=255, blank=True)
    tags = TaggableManager(verbose_name=u'Список тегов', blank=True)
    created = models.DateTimeField(verbose_name=u'Начало публикации', auto_now_add=True)
    changed = models.DateTimeField(verbose_name=u'Изменен', auto_now=True)
    deleted = models.DateTimeField(verbose_name=u'Дата окончания публикации', blank=True, null=True)
    meta_title = models.CharField(max_length=255, verbose_name=u'Title', null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, verbose_name=u'Keywords', null=True, blank=True)
    meta_description = models.TextField(max_length=255, verbose_name=u'Description', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.og_picture = opengraph(self)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Запись в блог'
        verbose_name_plural = 'Записи в блог'
        ordering = ['-date_post']

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255, unique=True, null=False)
    lead = models.TextField(verbose_name='Лидер-абзац', blank=True, null=True)
    text = RichTextField(null=True)
    date_start = models.DateTimeField(verbose_name='Дата публикации')
    date_change = models.DateTimeField(verbose_name='Дата последней правки', blank=True, null=True)
    date_finish = models.DateTimeField(verbose_name='Снять с публикации', blank=True, null=True)
    slug = AutoSlugField(populate_from='title')
    user_id = models.IntegerField(verbose_name='Порядковый номер пользователя', blank=True, null=True)
    picture = models.ImageField(verbose_name='Картинка к новости 450x258', upload_to=latin_filename, blank=True)
    is_hide = models.BooleanField(verbose_name='Скрыть с главной', default=False)
    is_rss = models.BooleanField(verbose_name='Отправить в rss', default=False)
    is_zen = models.BooleanField(verbose_name='Отправить в zen', default=False)
    is_delete = models.BooleanField(verbose_name='Новость удалена', default=False)
    is_video = models.BooleanField(verbose_name='Видеоновость', default=False)
    is_hold = models.BooleanField(verbose_name='Закреплена в рубрике', default=False)
    is_auto_delete = models.BooleanField(verbose_name='Автоуничтожение', default=False)
    is_main = models.BooleanField(verbose_name='Закреплена на главной', default=False)
    is_blog = models.BooleanField(verbose_name='Запись в блог', default=False)
    is_advert = models.BooleanField(verbose_name='Не показывать рекламу', default=False)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date_start']

    def __str__(self):
        return self.title


class Content(models.Model):
    txt_doc_id = models.IntegerField()
    txt_node_id = models.IntegerField()
    txt_title = models.CharField(max_length=255)
    txt_lead = RichTextField(null=True)
    txt_text = RichTextField(null=True)
    txt_author = models.CharField(max_length=255, blank=True, null=False)
    txt_issue = models.IntegerField()
    txt_clean_url = models.CharField(max_length=255)
    txt_publish_start = models.DateTimeField()
    txt_tags = models.CharField(max_length=1000, blank=True, null=False)

    class Meta:
        verbose_name = 'txt_title'
        verbose_name_plural = 'txt_title'
        ordering = ['-txt_publish_start']

    def __str__(self):
        return self.txt_title


class Person(models.Model):
    person_name = models.CharField(max_length=200)
    person_last_name = models.CharField(max_length=200, blank=True, null=False)
    person_status = models.CharField(max_length=200)
    person_bio = RichTextField(null=True)
    person_bio_short = RichTextField(null=True)
    person_foto = models.CharField(max_length=200, blank=True, null=False)
    person_clean_url = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'person_status'
        verbose_name_plural = 'person_status'
        ordering = ['person_last_name']

    def __str__(self):
        return self.person_status


class Site(models.Model):
    name = models.CharField(verbose_name='Название поля', max_length=200)
    value = models.CharField(verbose_name='Значение поля', max_length=200)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'
        ordering = ['-value']

    def __str__(self):
        return self.value
