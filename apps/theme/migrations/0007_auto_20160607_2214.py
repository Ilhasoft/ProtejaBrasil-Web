# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0006_themeinternationalization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='title',
            field=models.CharField(null=True, max_length=255, blank=True, verbose_name='Título', help_text='Insira o título do tema'),
        ),
    ]
