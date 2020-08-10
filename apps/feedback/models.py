from django.db import models


class FeedbackManager(models.Manager):
    def add_feedback(self, type, name, email, message, platform, version):
        PLATFORM_PERM = ['ios', 'android']

        if platform not in PLATFORM_PERM:
            raise (_('Platform invalid. Select iOS or Android.'))

        obj = self.model(
            type=type,
            name=name,
            email=email,
            message=message,
            platform=platform,
            version=version
        )
        obj.save(using=self._db)
        return obj

    def get_search(self, search):
        return super(FeedbackManager, self).get_queryset().filter(search).order_by('status', '-createdAt')


class Feedback(models.Model):
    TYPES_PERM = (
        ('doubt', 'Dúvida',),
        ('suggestion', 'Sugestão',),
        ('criticism', 'Crítica',),
        ('compliment', 'Elogio',),
    )

    PLATFORM_PERM = (
        ('android', 'Android'),
        ('ios', 'iOS'),
    )

    STATUS_PERM = (
        ('pending', 'Pendente',),
        ('resolved', 'Resolvido',)
    )

    type = models.CharField(verbose_name='Tipo', max_length=20, choices=TYPES_PERM, )
    name = models.CharField(verbose_name='Nome', max_length=255, )
    email = models.EmailField(verbose_name='E-mail', max_length=255, )
    message = models.TextField(verbose_name='Mensagem', )
    platform = models.CharField(verbose_name='Plataforma', max_length=20, null=True, blank=True, choices=PLATFORM_PERM, )
    version = models.CharField(verbose_name='Versão', max_length=100, null=True, blank=True, )
    status = models.CharField(default='pending', verbose_name='Status', max_length=100, null=True, blank=True, choices=STATUS_PERM, )
    createdAt = models.DateTimeField(verbose_name='Data de cadastro', auto_now_add=True, )
    objects = FeedbackManager()

    def __str__(self):
        return '{0} - {1}'.format(self.type, self.name)

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = verbose_name

    def get_type(self):
        TYPES = {
            'doubt': 'Dúvida',
            'suggestion': 'Sugestão',
            'criticism': 'Crítica',
            'compliment': 'Elogio'
        }
        try:
            type_ = TYPES[self.type]
        except:
            type_ = None

        return type_
