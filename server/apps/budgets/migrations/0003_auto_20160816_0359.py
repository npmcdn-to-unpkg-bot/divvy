# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-16 03:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0002_auto_20160816_0350'),
    ]

    operations = [
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('value', models.CharField(max_length=254)),
            ],
        ),
        migrations.AlterField(
            model_name='budget',
            name='icon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budgets.Icon'),
        ),
    ]
