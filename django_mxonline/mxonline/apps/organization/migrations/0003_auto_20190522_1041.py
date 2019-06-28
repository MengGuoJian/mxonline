# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-05-22 10:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20190516_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='course/%Y/%m', verbose_name='\u5934\u50cf'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CityDict', verbose_name='\u6240\u5728\u57ce\u5e02'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='\u6240\u5c5e\u673a\u6784'),
        ),
    ]
