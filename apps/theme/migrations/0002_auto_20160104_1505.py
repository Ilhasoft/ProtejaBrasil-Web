# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='color',
            field=models.CharField(verbose_name='Cor', max_length=10, null=True, help_text='Informe o código hexadecimal da cor', blank=True),
        ),
        migrations.AddField(
            model_name='theme',
            name='icon',
            field=sorl.thumbnail.fields.ImageField(verbose_name='Ícone', help_text='Selecione um ícone', null=True, max_length=255, upload_to='themes/icons', blank=True),
        ),
    ]
