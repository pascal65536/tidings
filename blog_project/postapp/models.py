import os

from ckeditor.fields import RichTextField
from django.conf.global_settings import MEDIA_URL
from django.db import models
from django.db.models.functions import datetime
from blog_project import utils


def latin_filename(instance, filename):
    f_folder = os.path.join(MEDIA_URL, '{:%Y/%m/%d}'.format(instance.date_post))
    salt = '{:%M%S}'.format(instance.date_post)
    part_of_name = filename.split(".")
    # f_name = utils.cyr_lat('_'.join(part_of_name[0:-1]))
    f_name = utils.cyr_lat(instance.title)
    f_ext = utils.cyr_lat(part_of_name[-1])
    return format('{}/{}/{}-{}.{}'.format('blog_picture', f_folder, f_name, salt, f_ext))


class Post(models.Model):
    title = models.CharField(verbose_name='Заголовок поста', max_length=255)
    lead = RichTextField(verbose_name='Лиер-абзац',)
    text = RichTextField(verbose_name='Тело поста',)
    date_post = models.DateTimeField(verbose_name='Дата публикации',
                                     default=datetime.datetime.now())
    picture = models.ImageField(verbose_name='Картинка для привлечения внимания', upload_to=latin_filename, blank=True)

    # txt_doc_id = models.IntegerField()
    # txt_node_id = models.IntegerField()
    # author = models.CharField(max_length=255, blank=True, null=False)
    # url = models.CharField(max_length=255, blank=True, null=False)
    # created = models.DateTimeField(blank=True, null=False)
    # changed = models.DateTimeField(blank=True, null=False)
    # deleted = models.DateTimeField(blank=True, null=False)

    class Meta:
        # db_table = 'post'
        verbose_name = 'Запись в блог'
        verbose_name_plural = 'Записи в блог'
        ordering = ['-date_post']

    def __str__(self):
        return self.title