# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0004_theme_sondha_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='order',
            field=models.IntegerField(null=True, default=0, blank=True, verbose_name='Ordem'),
        ),
    ]
