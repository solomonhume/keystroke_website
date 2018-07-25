# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-21 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('key_name', models.CharField(max_length=30)),
                ('release', models.IntegerField(default=0)),
                ('timestamp', models.BigIntegerField(default=0)),
            ],
        ),
    ]