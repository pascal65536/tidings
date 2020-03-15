from django.db import models
from newsproject.utils import latin_filename


class Photo(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    picture = models.ImageField(verbose_name='Картинка', upload_to=latin_filename, blank=True, null=True)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    changed = models.DateTimeField(verbose_name='Изменено', auto_now=True)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фото'
        ordering = ['-created']

    def __str__(self):
        return self.title
