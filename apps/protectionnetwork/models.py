# -*- coding: utf-8 -*-

from django.db import models
from django.shortcuts import get_object_or_404
from sorl.thumbnail.fields import ImageField
from geoposition.fields import GeopositionField
from apps.theme.models import Theme
from apps.uf.models import UF


class TypeManager(models.Manager):
    def get_search(self, search):
        return super(TypeManager, self).get_queryset().filter(search).order_by('-id')


class Type(models.Model):
    name = models.CharField(verbose_name='Nome', help_text='Informe o nome do tipo da rede de proteção',
                            max_length=255, unique=True, )
    color = models.CharField(verbose_name='Cor', help_text='Informe o código hexadecimal da cor', max_length=10,
                             null=True, blank=True, )
    icon = ImageField(verbose_name='Ícone', help_text='Selecione um ícone', max_length=255,
                      upload_to='protectionnetwork/types', null=True, blank=True, )
    date_joined = models.DateTimeField(verbose_name='Data de cadastro', help_text='Data de cadastro',
                                       auto_now_add=True, editable=False, null=True, )
    objects = TypeManager()

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'

    def get_icon(self):
        from protejabrasil import settings
        from sorl.thumbnail import get_thumbnail

        if self.icon:
            return 'http://{0}{1}'.format(settings.SITE_URL,
                                          get_thumbnail(self.icon, '60', quality=100, format='PNG').url)
        else:
            return None

    def get_default_language(self):
        return 'pt'


class TypeInternationalizationManager(models.Manager):
    def create(self, type_id, language, name):
        item = self.model(
            type_id=type_id,
            language=language,
            name=name
        )
        item.save(using=self._db)
        return item


class TypeInternationalization(models.Model):
    LANGUAGES = (
        ('pt', 'Português'),
        ('en', 'English'),
        ('es', 'Español'),
    )
    type = models.ForeignKey(Type, verbose_name='Tipo', related_name='info', )
    language = models.CharField(choices=LANGUAGES, verbose_name='Idioma', max_length=2, default='pt', )
    name = models.CharField(verbose_name='Nome', max_length=255, )
    date_joined = models.DateTimeField(verbose_name='Data de cadastro', help_text='Data de cadastro', auto_now_add=True, editable=False)
    objects = TypeInternationalizationManager()

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = 'Internacionalização'
        verbose_name_plural = verbose_name
        ordering = ('-language',)


class ProtectionNetworkManager(models.Manager):
    def get_search(self, user, search):
        states = user.states.all()
        states = [s.uf_id for s in states]

        themes = user.themes.all()
        themes = [t.theme_id for t in themes]

        queryset = super(ProtectionNetworkManager, self).get_queryset().filter(search).order_by('-id')

        filter = []

        for item in queryset:
            for ut in item.themes.all():
                theme = get_object_or_404(Theme, id=ut.theme_id)
                if theme.id in themes and item not in filter:
                    filter.append(item)

        new_filter = []

        for item_ in filter:
            state = get_object_or_404(UF, id=item_.state_id)
            if state.id in states and item_ not in new_filter:
                new_filter.append(item_)

        return new_filter

    def add_protectionnetwork(self, type, name, position, zipcode, address, neighborhood, city, state, contact, phone1,
                              phone2, email):
        item = self.model(
            type=type,
            name=name,
            position=position,
            zipcode=zipcode,
            address=address,
            neighborhood=neighborhood,
            city=city,
            state=state,
            contact=contact,
            phone1=phone1,
            phone2=phone2,
            email=email,
        )
        item.save(using=self._db)
        return item


class ProtectionNetwork(models.Model):
    type = models.ForeignKey(Type, verbose_name='Tipo', help_text='Selecione o tipo da rede de proteção', )
    name = models.CharField(verbose_name='Nome', max_length=255, )
    position = GeopositionField(verbose_name='Coordenadas', help_text='Selecione a localização no mapa.',
                                max_length=100, )
    zipcode = models.CharField(verbose_name='CEP', max_length=20, )
    address = models.CharField(verbose_name='Logradouro', max_length=255, )
    neighborhood = models.CharField(verbose_name='Bairro', max_length=255, )
    city = models.CharField(verbose_name='Cidade', max_length=255, )
    state = models.ForeignKey(UF, verbose_name='Estado', max_length=255, )
    contact = models.CharField(verbose_name='Contato', max_length=255, null=True, blank=True, )
    phone1 = models.CharField(verbose_name='Telefone 1', max_length=20, )
    phone2 = models.CharField(verbose_name='Telefone 2', max_length=20, null=True, blank=True, )
    email = models.CharField(verbose_name='E-mail', max_length=255, null=True, blank=True, )
    schedule = models.TextField(verbose_name='Horário', null=True, blank=True, )
    date_joined = models.DateTimeField(verbose_name='Data de cadastro', help_text='Data de cadastro',
                                       auto_now_add=True, editable=False)
    objects = ProtectionNetworkManager()

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = 'Rede de proteção'
        verbose_name_plural = 'Redes de proteção'

    def get_themes(self):
        all = self.themes.all()

        themes = []

        for theme in all:
            them = {}
            them['id'] = theme.theme.id
            them['name'] = theme.theme.title
            them['icon'] = theme.theme.get_icon()
            them['color'] = theme.theme.color
            them['description'] = theme.theme.description
            them['sondha_id'] = theme.theme.sondha_id
            themes.append(them)

        return themes

    def get_day(self):
        return self.operatingdays.all()

    def get_type(self):
        try:
            type_ = Type.objects.get(id=self.type.id)

            type = {}
            type['id'] = type_.id
            type['name'] = type_.name
            type['color'] = type_.color
            type['icon'] = type_.get_icon()

        except:
            type = None

        return type

    def get_state(self):
        try:
            state_ = UF.objects.get(id=self.state.id)

            state = {}
            state['initials'] = state_.initials
            state['title'] = state_.title

        except:
            state = None

        return state

    def get_position(self):
        try:
            position = {}
            position['lat'] = self.position.latitude
            position['long'] = self.position.longitude

        except:
            position = None

        return position

    def get_default_language(self):
        return 'pt'


class ProtectionNetworkInternationalizationManager(models.Manager):
    def create(self, protectionnetwork_id, language, name):
        item = self.model(
            protectionnetwork_id=protectionnetwork_id,
            language=language,
            name=name
        )
        item.save(using=self._db)
        return item


class ProtectionNetworkInternationalization(models.Model):
    LANGUAGES = (
        ('pt', 'Português'),
        ('en', 'English'),
        ('es', 'Español'),
    )
    protectionnetwork = models.ForeignKey(ProtectionNetwork, verbose_name='Rede de proteção', related_name='info', )
    language = models.CharField(choices=LANGUAGES, verbose_name='Idioma', max_length=2, default='pt', )
    name = models.CharField(verbose_name='Nome', max_length=255, )
    date_joined = models.DateTimeField(verbose_name='Data de cadastro', help_text='Data de cadastro', auto_now_add=True, editable=False)
    objects = ProtectionNetworkInternationalizationManager()

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = 'Internacionalização'
        verbose_name_plural = verbose_name
        ordering = ('-language',)


class ThemeProtectionNetworkManager(models.Manager):
    def add_theme_protectionnetwork(self, protectionnetwork, theme):
        item = self.model(
            protectionnetwork=protectionnetwork,
            theme=theme,
        )
        item.save(using=self._db)
        return item


class ThemeProtectionNetwork(models.Model):
    protectionnetwork = models.ForeignKey(ProtectionNetwork, verbose_name='Rede de proteção', related_name='themes', )
    theme = models.ForeignKey(Theme, verbose_name='Tema', )
    objects = ThemeProtectionNetworkManager()

    def __str__(self):
        return '{0}'.format(self.theme)

    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'


class OperatingDaysProtectionNetworkManager(models.Manager):
    def add_operatingdays_protectionnetwork(self, protectionnetwork, day):
        item = self.model(
            protectionnetwork=protectionnetwork,
            day=day,
        )
        item.save(using=self._db)
        return item


class OperatingDaysProtectionNetwork(models.Model):
    DAYS = (
        ('sunday', 'Domingo'),
        ('monday', 'Segunda-feira'),
        ('tuesday', 'Terça-feira'),
        ('wednesday', 'Quarta-feira'),
        ('thursday', 'Quinta-feira'),
        ('friday', 'Sexta-feira'),
        ('saturday', 'Sábado'),
    )

    protectionnetwork = models.ForeignKey(ProtectionNetwork, verbose_name='Rede de proteção',
                                          related_name='operatingdays', )
    day = models.CharField(verbose_name='Dia da semana', choices=DAYS, max_length=10, )
    objects = OperatingDaysProtectionNetworkManager()

    def __str__(self):
        return '{0}'.format(self.day)

    class Meta:
        verbose_name = 'Dia de atendimento'
        verbose_name_plural = 'Dias de atendimento'
