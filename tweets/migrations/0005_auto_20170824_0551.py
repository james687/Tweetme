# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-24 05:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_auto_20170811_1234'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ['-created_at']},
        ),
    ]