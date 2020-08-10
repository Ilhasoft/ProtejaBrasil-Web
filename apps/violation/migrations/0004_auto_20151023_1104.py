# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('violation', '0003_auto_20151022_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeviolation',
            name='theme',
            field=models.ForeignKey(null=True, verbose_name='Tema', blank=True, to='theme.Theme', help_text='Selecione o tema do tipo de violação.'),
        ),
    ]
