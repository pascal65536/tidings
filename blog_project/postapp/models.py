from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.functions import datetime


class Post(models.Model):
    # txt_doc_id = models.IntegerField()
    # txt_node_id = models.IntegerField()
    title = models.CharField(verbose_name='Заголовок поста', max_length=255)
    lead = RichTextField(verbose_name='Лиер-абзац',)
    text = RichTextField(verbose_name='Тело поста',)
    date_post = models.DateTimeField(verbose_name='Дата публикации',
                                     default=datetime.datetime.now())
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