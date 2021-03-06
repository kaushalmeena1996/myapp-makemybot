# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-12 13:10
from __future__ import unicode_literals

import botapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botapp', '0007_auto_20170811_2022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bot',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='bot',
            name='avtaar',
            field=models.ImageField(blank=True, null=True, upload_to=botapp.models.generate_filename),
        ),
        migrations.AlterField(
            model_name='bot',
            name='brain',
            field=models.FileField(blank=True, null=True, upload_to=botapp.models.generate_filename),
        ),
        migrations.AlterField(
            model_name='bot',
            name='chatlog',
            field=models.FileField(blank=True, null=True, upload_to=botapp.models.generate_filename),
        ),
    ]
