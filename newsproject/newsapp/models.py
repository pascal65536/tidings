from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from autoslug import AutoSlugField


class News(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255, unique=True, null=False)
    lead = models.TextField(verbose_name='Лидер-абзац', blank=True, null=True)
    text = RichTextField(null=True)
    date_start = models.DateTimeField(verbose_name='Дата публикации')
    date_start1 = models.DateTimeField(default=timezone.now, blank=True, null=True)
    date_finish = models.DateTimeField(verbose_name='Снять с публикации', blank=True, null=True)
    slug = AutoSlugField(populate_from='title')

    picture = models.ImageField(verbose_name='Картинка к новости', upload_to='news_picture/%Y/%m/%d', blank=True)

    is_hide = models.BooleanField(verbose_name='Скрыть с главной', default=False)
    is_rss = models.BooleanField(verbose_name='Отправить в rss', default=False)
    is_zen = models.BooleanField(verbose_name='Отправить в zen', default=False)
    is_delete = models.BooleanField(verbose_name='Новость удалена', default=False)
    is_video = models.BooleanField(verbose_name='Видеоновость', default=False)
    is_hold = models.BooleanField(verbose_name='Закреплена в рубрике', default=False)
    is_autodelete = models.BooleanField(verbose_name='Автоуничтожение', default=False)
    is_main = models.BooleanField(verbose_name='Закреплена на главной', default=False)
    is_blog = models.BooleanField(verbose_name='Запись в блог', default=False)
    is_advert = models.BooleanField(verbose_name='Не показывать рекламу', default=False)

    class Meta:
        db_table = 'news'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date_start']

    def __str__(self):
        return self.title
