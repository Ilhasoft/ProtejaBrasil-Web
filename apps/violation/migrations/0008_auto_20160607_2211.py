# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('violation', '0007_auto_20160607_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeviolation',
            name='action',
            field=models.TextField(null=True, help_text='Insira a ação a ser tomada.', verbose_name='Ação', blank=True),
        ),
    ]
