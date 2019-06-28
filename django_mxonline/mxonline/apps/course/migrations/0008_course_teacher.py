# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-05-28 12:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20190522_1041'),
        ('course', '0007_auto_20190527_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Teacher', verbose_name='\u8bfe\u7a0b\u673a\u6784'),
        ),
    ]
