# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0003_theme_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='sondha_id',
            field=models.IntegerField(blank=True, verbose_name='ID do SONDHA', null=True),
        ),
    ]
