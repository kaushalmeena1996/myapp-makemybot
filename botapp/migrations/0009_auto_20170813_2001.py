# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 14:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botapp', '0008_auto_20170812_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='avtaar',
            field=models.FilePathField(blank=True, null=True, path='/media/avtaar/bot_default.png'),
        ),
        migrations.AlterField(
            model_name='bot',
            name='brain',
            field=models.FilePathField(blank=True, null=True, path='/media/brain/brain_default.png'),
        ),
        migrations.AlterField(
            model_name='bot',
            name='chatlog',
            field=models.FilePathField(blank=True, null=True, path='/media/log/log_default.png'),
        ),
    ]
