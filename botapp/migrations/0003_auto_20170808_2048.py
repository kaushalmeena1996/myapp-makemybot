# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-08 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botapp', '0002_bot_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='desc',
            field=models.TextField(blank=True, max_length=256, null=True),
        ),
    ]