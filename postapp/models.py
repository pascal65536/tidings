from autoslug import AutoSlugField
from django.contrib.syndication.views import Feed
from django.db import models
from taggit.managers import TaggableManager
from newsproject.utils import delete_tags, latin_filename, opengraph
from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from django.urls import reverse
from django.views.generic import TemplateView
from photoapp.models import Photo


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
    text = models.TextField(verbose_name='Текст поста', blank=True, null=True)
    charter = models.ForeignKey(Charter, blank=True, null=True, verbose_name='Раздел', on_delete=models.SET_NULL)
    photo = models.ForeignKey(Photo, blank=True, null=True, verbose_name='Фото', on_delete=models.SET_NULL)
    date_post = models.DateTimeField(verbose_name='Дата публикации')
    picture = models.ImageField(verbose_name='Картинка для привлечения внимания', upload_to=latin_filename, blank=True, null=True)
    og_picture = models.CharField(verbose_name='Картинка для соцсетей', max_length=255, blank=True)
    tags = TaggableManager(verbose_name='Список тегов', blank=True)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    changed = models.DateTimeField(verbose_name='Изменено', auto_now=True)
    deleted = models.DateTimeField(verbose_name='Удалено', blank=True, null=True)
    meta_title = models.CharField(max_length=255, verbose_name='Title', null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, verbose_name='Keywords', null=True, blank=True)
    meta_description = models.TextField(max_length=255, verbose_name='Description', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    @classmethod
    def update_qs(cls, news_qs):
        photo_idx = set()
        charter_idx = set()

        for news in news_qs:
            photo_idx.add(news.photo_id)
            charter_idx.add(news.charter_id)

        photos = Photo.objects.in_bulk(photo_idx)
        charters = Charter.objects.in_bulk(charter_idx)

        for news in news_qs:
            news.photo_picture = None
            if news.photo:
                news.photo_picture = photos[news.photo_id].picture
            news.charter_title = None
            news.charter_slug = None
            if news.charter:
                news.charter_title = charters[news.charter_id].title
                news.charter_slug = charters[news.charter_id].slug
        return news_qs

    class Meta:
        verbose_name = 'Запись в блог'
        verbose_name_plural = 'Записи в блог'
        ordering = ['-date_post']

    def __str__(self):
        return self.title


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
