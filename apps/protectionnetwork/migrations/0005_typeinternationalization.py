# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from apps.protectionnetwork.models import TypeInternationalization


def populate_type_internationalization(apps, schema_editor):
    model = apps.get_model('protectionnetwork', 'Type')
    for row in model.objects.all():
        if row.info.all().count() == 0:
            TypeInternationalization.objects.create(row.id, 'pt', row.name)


class Migration(migrations.Migration):
    dependencies = [
        ('protectionnetwork', '0004_auto_20151022_1041'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeInternationalization',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('language', models.CharField(choices=[('pt', 'Português'), ('en', 'English'), ('es', 'Español')], default='pt', verbose_name='Idioma', max_length=2)),
                ('name', models.CharField(verbose_name='Nome', max_length=255)),
                ('date_joined', models.DateTimeField(auto_now_add=True, help_text='Data de cadastro', verbose_name='Data de cadastro')),
                ('type', models.ForeignKey(to='protectionnetwork.Type', verbose_name='Tipo', related_name='info')),
            ],
        ),
        migrations.RunPython(
            code=populate_type_internationalization,
            atomic=True
        )
    ]
