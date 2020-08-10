# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('violation', '0006_typeviolationinternationalization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeviolation',
            name='description',
            field=models.TextField(null=True, verbose_name='Descrição', blank=True, help_text='Insira uma descrição para o tipo de violação.'),
        ),
        migrations.AlterField(
            model_name='typeviolation',
            name='name',
            field=models.CharField(null=True, verbose_name='Nome', max_length=255, blank=True),
        ),
    ]
