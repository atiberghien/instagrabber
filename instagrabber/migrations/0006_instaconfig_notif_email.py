# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-29 04:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagrabber', '0005_auto_20190529_0455'),
    ]

    operations = [
        migrations.AddField(
            model_name='instaconfig',
            name='notif_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]