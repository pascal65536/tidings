from django.db import models


class Contacts(models.Model):
    name = models.TextField(verbose_name='Название офиса', blank='False', null=False)
    address_city = models.TextField(verbose_name='Индекс, город', blank='True', null=True)
    address_street = models.TextField(verbose_name='Улица, дом', blank='True', null=True)
    mail = models.TextField(verbose_name='Email', blank='True', null=True)
    phone = models.TextField(verbose_name='Телефон', blank='True', null=True)

    class Meta:
        db_table = 'contacts'
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['name']

    def __str__(self):
        return self.name
