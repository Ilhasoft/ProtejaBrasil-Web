# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Import',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('file', models.FileField(upload_to='importation')),
                ('date_joined', models.DateTimeField(help_text='Data de cadastro', verbose_name='Data de cadastro', auto_now_add=True)),
            ],
        ),
    ]
