# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-17 12:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordinem', '0005_hapcomments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hapcomments',
            name='comment_on',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_of', to='ordinem.Happening'),
        ),
    ]
