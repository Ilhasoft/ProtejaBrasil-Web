# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('violation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryTypeViolation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('category', models.CharField(max_length=100, choices=[('Violation', 'Violação'), ('InternetCrime', 'Crime na internet'), ('Accessibilty', 'Acessibilidade')], verbose_name='Categoria')),
                ('typeviolation', models.ForeignKey(related_name='categories', verbose_name='Tipo de violação', to='violation.TypeViolation')),
            ],
            options={
                'verbose_name_plural': 'Categorias do tipo de violação',
                'verbose_name': 'Categoria do tipo de violação',
            },
        ),
    ]
