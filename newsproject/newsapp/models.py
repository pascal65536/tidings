from django.db import models
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
import mymodule
from authorapp.models import Author
import datetime


def latin_filename(instance, filename):
    f_folder = '{:%Y/%m/%d}'.format(instance.date_start)
    salt = '{:%M%S}'.format(instance.date_start)
    part_of_name = filename.split(".")
    f_name = mymodule.cyr_lat('_'.join(part_of_name[0:-1]))
    f_ext = mymodule.cyr_lat(part_of_name[-1])
    return format('{}/{}/{}-{}.{}'.format('news_picture', f_folder, f_name, salt, f_ext))


class News(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255, unique=True, null=False)
    lead = models.TextField(verbose_name='Лидер-абзац', blank=True, null=True)
    text = RichTextField(null=True)
    date_start = models.DateTimeField(verbose_name='Дата публикации')
    date_change = models.DateTimeField(verbose_name='Дата последней правки', default=datetime.datetime.now(), blank=True, null=True)
    date_finish = models.DateTimeField(verbose_name='Снять с публикации', blank=True, null=True)
    slug = AutoSlugField(populate_from='title')
    user_id = models.IntegerField(verbose_name='Порядковый номер пользователя', blank=True, null=True)
    reporter = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='Репортер')
    photographer = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='Фотограф', blank=True, null=True, verbose_name='Фотограф')

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
        db_table = 'news'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date_start']

    def __str__(self):
        return self.title
