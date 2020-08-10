# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('violation', '0002_categorytypeviolation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorytypeviolation',
            name='category',
            field=models.CharField(max_length=100, choices=[('Violation', 'Violação'), ('InternetCrime', 'Crime na internet'), ('Accessibility', 'Acessibilidade')], verbose_name='Categoria'),
        ),
    ]
