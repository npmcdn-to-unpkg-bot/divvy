# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-16 03:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='icon',
            field=models.CharField(choices=[('cube', 'Cube'), ('car', 'Car'), ('bicycle', 'Bicycle'), ('plane', 'Airplane')], max_length=254),
        ),
    ]