from datetime import datetime, timezone
import uuid

from django.db import models

# Create your models here.
from django.urls import reverse

from advertapp.managers import AdvertManager
from newsproject.utils import latin_filename


class Advert(models.Model):
    """
    Реклама
    """

    CHOICE_POSITION = (
        ('top', 'Сверху'),
        ('bottom', 'Снизу'),
        ('content', 'Контент'),
        ('skyscraper', 'Небоскреб'),
    )
    CHOICE_COLOR = (
        ('primary', 'primary'),
        ('secondary', 'secondary'),
        ('success', 'success'),
        ('danger', 'danger'),
        ('warning', 'warning'),
        ('info', 'info'),
        ('light', 'light'),
        ('dark', 'dark'),
        ('white', 'white'),
        ('transparent', 'transparent'),
    )

    slug = models.UUIDField(verbose_name='Публичный код', default=uuid.uuid4, db_index=True, unique=True, editable=False)
    title = models.CharField(verbose_name='Название', max_length=255)
    image = models.ImageField(verbose_name='Картинка', upload_to=latin_filename, blank=True, null=True)
    color = models.CharField(verbose_name=u'Заливка', choices=CHOICE_COLOR, max_length=255)
    url = models.CharField(verbose_name=u'Ссылка', max_length=255, blank=True, null=True)
    html = models.TextField(verbose_name='Код', blank=True, null=True)
    position = models.CharField(verbose_name='Положение', choices=CHOICE_POSITION, max_length=255)
    counter_json = models.JSONField(verbose_name='Клики по рекламе', default=dict)
    date_start = models.DateTimeField(verbose_name='Дата начала')
    date_stop = models.DateTimeField(verbose_name='Дата конца')
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    changed = models.DateTimeField(verbose_name='Changed', auto_now=True)
    deleted = models.DateTimeField(verbose_name='Deleted', blank=True, null=True, help_text='Set datetime, when it was deleted')

    objects = AdvertManager()

    @property
    def is_present(self):
        """
        Agreement is acting now?
        :return:
        """
        today = datetime.now(timezone.utc)
        return self.date_start < today < self.date_stop

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламы'
        ordering = ['-date_start']
