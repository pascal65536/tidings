# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-15 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorapp', '0012_auto_20180916_0135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='mail',
            field=models.CharField(blank=True, max_length=25, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='author',
            name='phone',
            field=models.CharField(blank=True, max_length=25, verbose_name='Телефон'),
        ),
    ]