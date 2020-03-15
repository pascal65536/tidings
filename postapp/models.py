# coding=utf-8
import os
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.syndication.views import Feed
from django.db import models
from PIL import Image, ImageDraw, ImageFont
from taggit.managers import TaggableManager
from newsproject.utils import cyr_lat, delete_tags, latin_filename, opengraph
from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from django.urls import reverse
from django.views.generic import TemplateView


#     sidebar_cache = 'sidebar_cache.json'
#     file_cache = os.path.join(directory, sidebar_cache)
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#
#     if os.path.isfile(file_cache):
#         with open(file_cache, 'r') as f:
#             return json.load(f)

class Charter(models.Model):
    title = models.CharField(verbose_name='Название', max_length=20)
    lead = models.TextField(verbose_name='Лидер-абзац')
    order = models.IntegerField(verbose_name='Сортировка', default=1)
    slug = AutoSlugField(populate_from='title')
    text = models.TextField(verbose_name='Описание раздела', blank=True, null=True)
    picture = models.ImageField(verbose_name='Картинка раздела', upload_to=latin_filename, blank=True, null=True)
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
    text = RichTextField(config_name='default')
    charter = models.ForeignKey(Charter, blank=True, null=True, verbose_name='Раздел', on_delete=models.SET_NULL)
    date_post = models.DateTimeField(verbose_name='Дата начала публикации')
    picture = models.ImageField(verbose_name='Картинка для привлечения внимания', upload_to=latin_filename, blank=True, null=True)
    og_picture = models.CharField(verbose_name='Картинка для соцсетей', max_length=255, blank=True)
    tags = TaggableManager(verbose_name='Список тегов', blank=True)
    created = models.DateTimeField(verbose_name='Начало публикации', auto_now_add=True)
    changed = models.DateTimeField(verbose_name='Изменен', auto_now=True)
    deleted = models.DateTimeField(verbose_name='Дата окончания публикации', blank=True, null=True)
    meta_title = models.CharField(max_length=255, verbose_name='Title', null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, verbose_name='Keywords', null=True, blank=True)
    meta_description = models.TextField(max_length=255, verbose_name='Description', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.og_picture = opengraph(self)
        super(Post, self).save(*args, **kwargs)

        if self.picture:
            extension = str(self.picture.path).rsplit('.', 1)[1]
            filename = str(self.picture.path).rsplit(os.sep, 1)[1].rsplit('.', 1)[0]
            fullpath = str(self.picture.path).rsplit(os.sep, 1)[0]
            if extension in ['jpg', 'jpeg', 'png']:
                im = Image.open(str(self.picture.path))
                pic_width = 800
                pic_height = 600
                (w, h) = im.size
                if w/h < pic_width/pic_height:
                    percent = pic_width/w
                else:
                    percent = pic_height/h
                width = int(w * percent)
                height = int(h * percent)
                im = im.resize((width, height), Image.ANTIALIAS)
                yc = int((height - pic_height)/2)
                xc = 0
                im = im.crop((xc, yc, xc + pic_width, yc + pic_height))
                im.save('{}/{}.{}'.format(fullpath, filename, extension), format='JPEG', dpi=[72, 72])
                super(Post, self).save(*args, **kwargs)
            return

    class Meta:
        verbose_name = 'Запись в блог'
        verbose_name_plural = 'Записи в блог'
        ordering = ['-date_post']

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255, unique=True, null=False)
    lead = models.TextField(verbose_name='Лидер-абзац', blank=True, null=True)
    text = models.TextField(null=True)
    date_start = models.DateTimeField(verbose_name='Дата публикации')
    date_change = models.DateTimeField(verbose_name='Дата последней правки', blank=True, null=True)
    date_finish = models.DateTimeField(verbose_name='Снять с публикации', blank=True, null=True)
    slug = AutoSlugField(populate_from='title')
    user_id = models.IntegerField(verbose_name='Порядковый номер пользователя', blank=True, null=True)
    picture = models.ImageField(verbose_name='Картинка к новости 450x258', upload_to=latin_filename, blank=True, null=True)
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
    txt_lead = models.TextField(null=True)
    txt_text = models.TextField(null=True)
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
    person_bio = models.TextField(null=True)
    person_bio_short = models.TextField(null=True)
    person_foto = models.CharField(max_length=200, blank=True, null=False)
    person_clean_url = models.CharField(max_length=200)

    def __str__(self):
        return self.person_status

    class Meta:
        verbose_name = 'person_status'
        verbose_name_plural = 'person_status'
        ordering = ['person_last_name']


class Site(models.Model):
    name = models.CharField(verbose_name='Название поля', max_length=200)
    value = models.TextField(verbose_name='Значение поля', blank=True, null=True)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'
        ordering = ['-value']

    def __str__(self):
        return self.value


class PostSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.5

    def items(self):
        return Post.objects.filter(deleted__isnull=True, date_post__lte=timezone.now()).order_by('-date_post')

    def lastmod(self, obj):
        return obj.date_post

    def location(self, obj):
        return "/detail/%d" % obj.pk


class PostFeed(Feed):
    title = "Мелочи жизни"
    description = "Последние статьи сайта Мелочи жизни"
    link = "/"

    def items(self):
        return Post.objects.filter(deleted__isnull=True, date_post__lte=timezone.now()).order_by('-date_post')[0:25]

    def item_title(self, obj):
        return obj.title

    def item_description(self, obj):
        return obj.lead

    def item_link(self, obj):
        return "/detail/%d" % obj.pk


class YandexRss(TemplateView):
    template_name = 'rss/yandex.xml'
    filter = {
        'deleted': None
    }

    def get_context_data(self, **kwargs):
        ctx = super(YandexRss, self).get_context_data(**kwargs)
        post_qs = Post.objects.filter(deleted__isnull=True, date_post__lte=timezone.now()).order_by('-date_post')[0:25]
        for post in post_qs:
            post.title = delete_tags(post.title)
            post.lead = '<![CDATA[{}]]>'.format(delete_tags(post.lead))
            post.text = '<![CDATA[{}]]>'.format(delete_tags(post.text))
        ctx['object_list'] = post_qs
        ctx['static'] = settings.STATIC_URL
        ctx['media'] = settings.MEDIA_URL
        ctx['host'] = Site.objects.get(name='host')
        ctx['sitename'] = Site.objects.get(name='sitename')
        ctx['description'] = Site.objects.get(name='description')
        return ctx

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'text/xml; charset=UTF-8'
        return super(YandexRss, self).render_to_response(context, **response_kwargs)


class YandexDzenRss(TemplateView):
    template_name = 'rss/zen.xml'
    filter = {
        'deleted': None,
    }

    def get_context_data(self, **kwargs):
        ctx = super(YandexDzenRss, self).get_context_data(**kwargs)
        post_qs = Post.objects.filter(deleted__isnull=True, date_post__lte=timezone.now()).order_by('-date_post')[0:25]
        for post in post_qs:
            post.title = delete_tags(post.title)
            post.lead = '<![CDATA[{}]]>'.format(delete_tags(post.lead))
            post.text = '<![CDATA[{}]]>'.format(delete_tags(post.text))
        ctx['object_list'] = post_qs
        ctx['static'] = settings.STATIC_URL
        ctx['media'] = settings.MEDIA_URL
        ctx['host'] = Site.objects.get(name='host')
        ctx['sitename'] = Site.objects.get(name='sitename')
        ctx['description'] = Site.objects.get(name='description')
        return ctx

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'text/xml; charset=UTF-8'
        return super(YandexDzenRss, self).render_to_response(context, **response_kwargs)


class YandexTurboRss(TemplateView):
    template_name = 'rss/turbo.xml'
    filter = {
        'deleted': None,
    }

    def get_context_data(self, **kwargs):
        ctx = super(YandexTurboRss, self).get_context_data(**kwargs)
        post_qs = Post.objects.filter(deleted__isnull=True, date_post__lte=timezone.now()).order_by('date_post')[0:3]
        ctx['object_list'] = post_qs
        ctx['static'] = settings.STATIC_URL
        ctx['media'] = settings.MEDIA_URL
        ctx['host'] = Site.objects.get(name='host')
        ctx['sitename'] = Site.objects.get(name='sitename')
        ctx['description'] = Site.objects.get(name='description')
        return ctx

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'text/xml; charset=UTF-8'
        return super(YandexTurboRss, self).render_to_response(context, **response_kwargs)
