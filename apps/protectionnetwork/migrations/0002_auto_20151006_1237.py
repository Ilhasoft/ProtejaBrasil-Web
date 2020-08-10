# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protectionnetwork', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data de cadastro', help_text='Data de cadastro'),
        ),
    ]
