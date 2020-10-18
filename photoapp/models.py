import os

from django.db import models
from taggit.managers import TaggableManager
from PIL import Image
from newsproject.utils import latin_filename
from django.utils.safestring import mark_safe


class Photo(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    tags = TaggableManager(verbose_name='Список тегов', blank=True)
    description = models.CharField(verbose_name='Описание', max_length=255, blank=True, null=True)
    picture = models.ImageField(verbose_name='Картинка', upload_to=latin_filename, blank=True, null=True)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    changed = models.DateTimeField(verbose_name='Изменено', auto_now=True)
    deleted = models.DateTimeField(verbose_name='Удалено', blank=True, null=True)

    def image_img(self):
        """
        Вывод картинок в админке
        """
        if self.picture:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.picture.url))
        else:
            return '(Нет изображения)'

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

        if self.picture and os.path.exists(self.picture.path):
            extension = str(self.picture.path).rsplit('.', 1)[1]
            filename = str(self.picture.path).rsplit(os.sep, 1)[1].rsplit('.', 1)[0]
            fullpath = str(self.picture.path).rsplit(os.sep, 1)[0]
            if extension in ['jpg', 'jpeg', 'png']:
                im = Image.open(str(self.picture.path))
                pic_width = 800
                pic_height = 600
                (w, h) = im.size
                if w/h < pic_width/pic_height:
                    percent = pic_width/w
                else:
                    percent = pic_height/h
                width = int(w * percent)
                height = int(h * percent)
                im = im.resize((width, height), Image.ANTIALIAS)
                yc = int((height - pic_height)/2)
                xc = 0
                im = im.crop((xc, yc, xc + pic_width, yc + pic_height))
                im.save('{}/{}.{}'.format(fullpath, filename, extension), format='JPEG', dpi=[72, 72])
                super(Photo, self).save(*args, **kwargs)
            return

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фото'
        ordering = ['-created']
