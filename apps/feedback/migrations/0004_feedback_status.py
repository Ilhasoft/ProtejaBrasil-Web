# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_auto_20160215_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendente'), ('resolved', 'Resolvido')], default='pending', null=True, max_length=100, verbose_name='Status', blank=True),
        ),
    ]
