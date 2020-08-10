# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protectionnetwork', '0003_auto_20151006_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protectionnetwork',
            name='email',
            field=models.CharField(max_length=255, null=True, blank=True, verbose_name='E-mail'),
        ),
    ]
