from django.db import models
from sorl.thumbnail.fields import ImageField


class Theme(models.Model):
    title = models.CharField(verbose_name='Título', help_text='Insira o título do tema', max_length=255, null=True, blank=True, )
    color = models.CharField(verbose_name='Cor', help_text='Informe o código hexadecimal da cor', max_length=10, null=True, blank=True, )
    icon = ImageField(verbose_name='Ícone', help_text='Selecione um ícone', max_length=255, upload_to='themes/icons', null=True, blank=True, )
    description = models.TextField(verbose_name='Descrição', null=True, blank=True, )
    order = models.IntegerField(verbose_name='Ordem', null=True, blank=True, default=0, )
    date_joined = models.DateTimeField(verbose_name='Data de cadastro', help_text='Data de cadastro', auto_now_add=True, editable=False)
    sondha_id = models.IntegerField(verbose_name='ID do SONDHA', null=True, blank=True, )

    def __str__(self):
        return "{0}".format(self.title)

    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'

    def get_icon(self):
        from protejabrasil import settings
        from sorl.thumbnail import get_thumbnail

        if self.icon:
            return 'http://{0}{1}'.format(settings.SITE_URL, get_thumbnail(self.icon, '60', quality=100, format='PNG').url)
        else:
            return None

    def get_default_language(self):
        return 'pt'


class ThemeInternationalizationManager(models.Manager):
    def create(self, theme_id, language, title, description):
        item = self.model(
            theme_id=theme_id,
            language=language,
            title=title,
            description=description
        )
        item.save(using=self._db)
        return item


class ThemeInternationalization(models.Model):
    LANGUAGES = (
        ('pt', 'Português'),
        ('en', 'English'),
        ('es', 'Español'),
    )
    theme = models.ForeignKey(Theme, verbose_name='Tema', help_text='Tema', related_name='info', )
    language = models.CharField(choices=LANGUAGES, verbose_name='Idioma', max_length=2, default='pt', )
    title = models.CharField(verbose_name='Título', help_text='Insira o título do tema', max_length=255, )
    description = models.TextField(verbose_name='Descrição', null=True, blank=True, )
    date_joined = models.DateTimeField(verbose_name='Data de cadastro', help_text='Data de cadastro', auto_now_add=True, editable=False)
    objects = ThemeInternationalizationManager()

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'Internacionalização'
        verbose_name_plural = verbose_name
        ordering = ('-language',)
