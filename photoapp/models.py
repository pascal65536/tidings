from django.db import models
from newsproject.utils import latin_filename
from django.utils.safestring import mark_safe


class Photo(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    picture = models.ImageField(verbose_name='Картинка', upload_to=latin_filename, blank=True, null=True)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    changed = models.DateTimeField(verbose_name='Изменено', auto_now=True)

    def image_img(self):
        """
        Вывод картинок в админке
        """
        if self.picture:

            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.picture.url))
        else:
            return '(Нет изображения)'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фото'
        ordering = ['-created']
