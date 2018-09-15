from django.db import models


class Author(models.Model):
    name = models.TextField(verbose_name='Фамилия и имя', blank='False', null=False)
    city = models.TextField(verbose_name='Страна, город', blank='False', null=False)
    nickname = models.TextField(verbose_name='Прозвище', blank='False', null=False)
    mail = models.TextField(verbose_name='Email', blank='True', null=True)
    phone = models.TextField(verbose_name='Телефон', blank='True', null=True)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='author_avatar', blank=True)
    background = models.ImageField(verbose_name='Фон', upload_to='author_background', blank=True)

    class Meta:
        db_table = 'author'
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['name']

    def __str__(self):
        return self.name
