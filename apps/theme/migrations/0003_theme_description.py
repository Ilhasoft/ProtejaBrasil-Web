# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0002_auto_20160104_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='description',
            field=models.TextField(blank=True, verbose_name='Descrição', null=True),
        ),
    ]
