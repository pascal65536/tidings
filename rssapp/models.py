from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class BaseUrl(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255, blank=True, null=True)
    url = models.CharField(verbose_name='Ссылка', max_length=255, blank=True, null=True)
    feed = models.CharField(verbose_name='RSS', max_length=255, unique=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сайт'
        verbose_name_plural = 'Сайты'
        ordering = ['-name']


class Content(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255, unique=True, null=False)
    lead = models.TextField(verbose_name='Лидер-абзац', blank=True, null=True)
    text = models.TextField(verbose_name='Текст', blank=True, null=True)

    tr_title = models.CharField(verbose_name='Англ. Заголовок', max_length=255, blank=True, null=True)
    tr_lead = models.TextField(verbose_name='Англ. Лидер-абзац', blank=True, null=True)
    tr_text = models.TextField(verbose_name='Англ. Текст', blank=True, null=True)

    baseurl = models.ForeignKey(BaseUrl, on_delete=models.CASCADE)
    url = models.CharField(verbose_name='Ссылка', max_length=255, unique=True, null=False)
    pic = models.CharField(verbose_name='Картинка', max_length=255, blank=True, null=True)

    is_marked = models.BooleanField(verbose_name='Отмечено', default=False)
    is_read = models.BooleanField(verbose_name='Прочитано', default=False)
    published = models.DateTimeField(verbose_name=u'Опубликовано', auto_now_add=True)

    created = models.DateTimeField(verbose_name=u'Создан', auto_now_add=True)
    changed = models.DateTimeField(verbose_name=u'Изменен', auto_now=True)
    deleted = models.DateTimeField(verbose_name=u'Удален', blank=True, null=True)

    # date_start = models.DateTimeField(verbose_name='Дата публикации')
    # date_change = models.DateTimeField(verbose_name='Дата последней правки', blank=True, null=True)
    # date_finish = models.DateTimeField(verbose_name='Снять с публикации', blank=True, null=True)
    # slug = AutoSlugField(populate_from='title')
    # user_id = models.IntegerField(verbose_name='Порядковый номер пользователя', blank=True, null=True)
    # picture = models.ImageField(verbose_name='Картинка к новости 450x258', upload_to=latin_filename, blank=True, null=True)
    # is_hide = models.BooleanField(verbose_name='Скрыть с главной', default=False)
    # is_rss = models.BooleanField(verbose_name='Отправить в rss', default=False)
    # is_zen = models.BooleanField(verbose_name='Отправить в zen', default=False)
    # is_delete = models.BooleanField(verbose_name='Новость удалена', default=False)
    # is_video = models.BooleanField(verbose_name='Видеоновость', default=False)
    # is_hold = models.BooleanField(verbose_name='Закреплена в рубрике', default=False)
    # is_auto_delete = models.BooleanField(verbose_name='Автоуничтожение', default=False)
    # is_main = models.BooleanField(verbose_name='Закреплена на главной', default=False)
    # is_blog = models.BooleanField(verbose_name='Запись в блог', default=False)
    # is_advert = models.BooleanField(verbose_name='Не показывать рекламу', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created']


class Article(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    pic = ThumbnailerImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['id']
