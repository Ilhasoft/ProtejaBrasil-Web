# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protectionnetwork', '0002_auto_20151006_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protectionnetwork',
            name='zipcode',
            field=models.CharField(verbose_name='CEP', max_length=20),
        ),
    ]
