# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='platform',
            field=models.CharField(verbose_name='Plataforma', max_length=20, null=True, blank=True, choices=[('Android', 'Android'), ('iOS', 'iOS')]),
        ),
        migrations.AddField(
            model_name='feedback',
            name='version',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Versão'),
        ),
    ]
