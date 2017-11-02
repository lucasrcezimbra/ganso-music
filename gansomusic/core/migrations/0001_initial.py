# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-02 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255, verbose_name='URL')),
                ('title', models.CharField(max_length=200, verbose_name='título')),
                ('artist', models.CharField(max_length=200, verbose_name='artista')),
                ('genre', models.CharField(max_length=100, verbose_name='gênero')),
                ('file', models.FileField(upload_to='')),
            ],
        ),
    ]
