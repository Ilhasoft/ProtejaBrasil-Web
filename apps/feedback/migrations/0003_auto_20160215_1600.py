# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20160215_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='platform',
            field=models.CharField(null=True, blank=True, verbose_name='Plataforma', choices=[('android', 'Android'), ('ios', 'iOS')], max_length=20),
        ),
    ]
