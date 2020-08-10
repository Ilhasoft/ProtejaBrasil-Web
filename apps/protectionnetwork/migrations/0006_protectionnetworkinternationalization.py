# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from apps.protectionnetwork.models import ProtectionNetworkInternationalization


def populate_protectionnetwork_internationalization(apps, schema_editor):
    model = apps.get_model('protectionnetwork', 'ProtectionNetwork')
    for row in model.objects.all():
        if row.info.all().count() == 0:
            ProtectionNetworkInternationalization.objects.create(row.id, 'pt', row.name)


class Migration(migrations.Migration):
    dependencies = [
        ('protectionnetwork', '0005_typeinternationalization'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProtectionNetworkInternationalization',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('language', models.CharField(default='pt', max_length=2, choices=[('pt', 'Português'), ('en', 'English'), ('es', 'Español')], verbose_name='Idioma')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('date_joined', models.DateTimeField(help_text='Data de cadastro', auto_now_add=True, verbose_name='Data de cadastro')),
                ('protectionnetwork', models.ForeignKey(verbose_name='Rede de proteção', to='protectionnetwork.ProtectionNetwork', related_name='info')),
            ],
        ),
        migrations.RunPython(
            code=populate_protectionnetwork_internationalization,
            atomic=True
        ),
    ]
