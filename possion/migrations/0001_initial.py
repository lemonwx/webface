# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 10:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='possion/%Y/%m')),
                ('add_time', models.DateTimeField(default=datetime.datetime(2017, 10, 25, 10, 57, 25, 293388))),
            ],
        ),
        migrations.CreateModel(
            name='PossionTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pre_img_id', models.IntegerField(default=0)),
                ('bak_img_id', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=0)),
                ('tgt_img_path', models.ImageField(upload_to='target/%Y/%m')),
            ],
        ),
    ]
