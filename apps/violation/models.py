from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import get_object_or_404
from sorl.thumbnail.fields import ImageField
from apps.protectionnetwork.models import Type
from apps.theme.models import Theme


class TypeViolationManager(models.Manager):
    def get_search(self, user, search):
        themes = user.themes.all()
        themes = [t.theme_id for t in themes]

        if search:
            queryset = super(TypeViolationManager, self).get_queryset().filter(search).order_by('-id')
        else:
            queryset = super(TypeViolationManager, self).get_queryset().order_by('-id')

        filter = []

        for item in queryset:
            if not item.theme_id:
                filter.append(item)
            else:
                theme = get_object_or_404(Theme, id=item.theme_id)
                if theme.id in themes and item not in filter:
                    filter.append(item)

        filter_ids = [f.id for f in filter]
        queryset = super(TypeViolationManager, self).get_queryset().filter(pk__in=filter_ids).order_by('-id')

        return queryset


class TypeViolation(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=255, null=True, blank=True, )
    description = models.TextField(verbose_name='Descrição', help_text='Insira uma descrição para o tipo de violação.', null=True, blank=True, )
    theme = models.ForeignKey(Theme, verbose_name='Tema', help_text='Selecione o tema do tipo de violação.', null=True, blank=True, )
    color = models.CharField(verbose_name='Cor', help_text='Informe o código hexadecimal da cor', max_length=10, null=True, blank=True, )
    icon = ImageField(verbose_name='Ícone', help_text='Selecione um ícone', max_length=255, upload_to='violation/types', null=True, blank=True, )
    action = models.TextField(verbose_name='Ação', help_text='Insira a ação a ser tomada.', null=True, blank=True, )
    date_joined = models.DateTimeField(verbose_name='Data de cadastro', help_text='Data de cadastro', auto_now_add=True, editable=False)
    objects = TypeViolationManager()

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'

    def get_icon(self):
        from protejabrasil import settings
        from sorl.thumbnail import get_thumbnail

        if self.icon:
            return 'http://{0}{1}'.format(settings.SITE_URL, get_thumbnail(self.icon, '60', quality=100, format='PNG').url)
        else:
            return None

    def get_types(self):
        all = self.typesprotectionnetwork.all()

        types = []

        for type in all:
            typ = {}
            typ['id'] = type.typeprotectionnetwork.id
            typ['name'] = type.typeprotectionnetwork.name
            typ['color'] = type.typeprotectionnetwork.color
            typ['icon'] = type.typeprotectionnetwork.get_icon()
            types.append(typ)

        return types

    def get_types_id(self):
        return [type.typeprotectionnetwork.id for type in self.typesprotectionnetwork.all()]

    def get_theme(self):
        try:
            theme_ = Theme.objects.get(id=self.theme_id)

            theme = {}
            theme['id'] = theme_.id
            theme['title'] = theme_.title
            theme['icon'] = theme_.get_icon()
            theme['color'] = theme_.color
            theme['description'] = theme_.description
            theme['sondha_id'] = theme_.sondha_id

        except:
            theme = None

        return theme

    def get_categories(self):
        all = self.categories.all()

        categories = []

        for category in all:
            cvt = {}
            cvt['category'] = category.category
            categories.append(cvt)

        return categories

    def get_default_language(self):
        return 'pt'


class TypeViolationInternationalizationManager(models.Manager):
    def create(self, typeviolation_id, language, name, description, action):
        item = self.model(
            typeviolation_id=typeviolation_id,
            language=language,
            name=name,
            description=description,
            action=action
        )
        item.save(using=self._db)
        return item


class TypeViolationInternationalization(models.Model):
    LANGUAGES = (
        ('pt', 'Português'),
        ('en', 'English'),
        ('es', 'Español'),
    )
    typeviolation = models.ForeignKey(TypeViolation, verbose_name='Tipo de violação', related_name='info', )
    language = models.CharField(choices=LANGUAGES, verbose_name='Idioma', max_length=2, default='pt', )
    name = models.CharField(verbose_name='Nome', max_length=255, )
    description = models.TextField(verbose_name='Descrição', help_text='Insira uma descrição para o tipo de violação.', )
    action = models.TextField(verbose_name='Ação', help_text='Insira a ação a ser tomada.', null=True, blank=True, )
    date_joined = models.DateTimeField(verbose_name='Data de cadastro', help_text='Data de cadastro', auto_now_add=True, editable=False)
    objects = TypeViolationInternationalizationManager()

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = 'Internacionalização'
        verbose_name_plural = verbose_name
        ordering = ('-language',)


class CategoryTypeViolationManager(models.Manager):
    def add_category_typeviolation(self, typeviolation, category):
        ITEMS_PERM = ['Violation', 'InternetCrime', 'Accessibility']

        if category not in ITEMS_PERM:
            raise ValidationError('Valor não permitido.')

        item = self.model(
            typeviolation=typeviolation,
            category=category,
        )
        item.save(using=self._db)
        return item


class CategoryTypeViolation(models.Model):
    TYPES_PERM = (
        ('Violation', 'Violação'),
        ('InternetCrime', 'Crime na internet'),
        ('Accessibility', 'Acessibilidade'),
    )

    typeviolation = models.ForeignKey(TypeViolation, verbose_name='Tipo de violação', related_name='categories', )
    category = models.CharField(verbose_name='Categoria', choices=TYPES_PERM, max_length=100, )
    objects = CategoryTypeViolationManager()

    def __str__(self):
        return '{0}'.format(self.category)

    class Meta:
        verbose_name = 'Categoria do tipo de violação'
        verbose_name_plural = 'Categorias do tipo de violação'


class TypeProtectionNetworkManager(models.Manager):
    def add_type_protectionnetwork(self, typeviolation, typeprotectionnetwork):
        item = self.model(
            typeviolation=typeviolation,
            typeprotectionnetwork=typeprotectionnetwork,
        )
        item.save(using=self._db)
        return item


class TypeProtectionNetwork(models.Model):
    typeviolation = models.ForeignKey(TypeViolation, verbose_name='Tipo de violação',
                                      related_name='typesprotectionnetwork')
    typeprotectionnetwork = models.ForeignKey(Type, verbose_name='Tipo de rede de proteção', )
    objects = TypeProtectionNetworkManager()

    def __str__(self):
        return '{0}'.format(self.typeprotectionnetwork)

    class Meta:
        verbose_name = 'Tipo de rede de proteção da violação'
        verbose_name_plural = 'Tipos de rede de proteção da violação'
