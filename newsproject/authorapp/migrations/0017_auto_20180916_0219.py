# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-15 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorapp', '0016_auto_20180916_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='social_network_1_logo',
            field=models.CharField(blank=True, max_length=30, verbose_name='Логотип 1'),
        ),
    ]
