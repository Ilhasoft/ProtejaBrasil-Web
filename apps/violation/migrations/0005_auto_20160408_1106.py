# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('violation', '0004_auto_20151023_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeviolation',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
    ]
