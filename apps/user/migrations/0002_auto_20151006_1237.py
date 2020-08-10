# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_auth',
            field=models.ForeignKey(related_name='user_insert', null=True, blank=True, verbose_name='Usuário de cadastro', to=settings.AUTH_USER_MODEL, help_text='Usuário que o cadastro'),
        ),
    ]
