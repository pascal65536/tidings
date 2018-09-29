from django.db import models
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField


class Author(models.Model):
    name = models.CharField(verbose_name='Фамилия и имя', max_length=250, unique=True, null=True)
    city = models.CharField(verbose_name='Страна, город', max_length=250, unique=False, null=True)
    slug = AutoSlugField(verbose_name='Прозвище', populate_from='name')
    mail = models.CharField(verbose_name='Email', max_length=25, unique=False, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=25, unique=False, blank=True)
    avatar = models.ImageField(verbose_name='Аватар 95x95', upload_to='author_avatar', blank=True)
    background = models.ImageField(verbose_name='Фон 270x115', upload_to='author_background', blank=True)
    background_page = models.ImageField(verbose_name='Фон страницы 1000x226', upload_to='author_background_page', blank=True)
    about = RichTextField(null=True)

    is_hide = models.BooleanField(verbose_name='Скрыть', default=False)
    order = models.IntegerField(verbose_name='Приоритет', default=10)

    social_network_1 = models.CharField(verbose_name='Социальная сеть 1', max_length=200, null=False, blank=True)
    social_network_2 = models.CharField(verbose_name='Социальная сеть 2', max_length=200, null=False, blank=True)
    social_network_3 = models.CharField(verbose_name='Социальная сеть 3', max_length=200, null=False, blank=True)
    social_network_4 = models.CharField(verbose_name='Социальная сеть 4', max_length=200, null=False, blank=True)
    social_network_5 = models.CharField(verbose_name='Социальная сеть 5', max_length=200, null=False, blank=True)
    social_network_6 = models.CharField(verbose_name='Социальная сеть 6', max_length=200, null=False, blank=True)

    class Meta:
        db_table = 'author'
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['name']

    def __str__(self):
        return self.name
