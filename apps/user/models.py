# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.shortcuts import get_object_or_404
from django.utils import timezone
from apps.permission.models import Permission
from apps.theme.models import Theme
from apps.uf.models import UF


class UsersManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None):
        if not username:
            raise ValueError('Os usuários devem ter um username.')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password):
        user = self.create_user(username,
                                first_name=first_name,
                                last_name=last_name,
                                email=email,
                                password=password
                                )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_search(self, user, search):
        states = user.states.all()
        states = [s.uf_id for s in states]

        themes = user.themes.all()
        themes = [t.theme_id for t in themes]

        queryset = super(UsersManager, self).get_queryset().filter(search).order_by('-id')

        filter = []

        for user in queryset:
            for ut in user.themes.all():
                theme = get_object_or_404(Theme, id=ut.theme_id)
                if theme.id in themes and user not in filter:
                    filter.append(user)

        new_filter = []

        for user_ in filter:
            for us in user_.states.all():
                state = get_object_or_404(UF, id=us.uf_id)
                if state.id in states and user_ not in new_filter:
                    new_filter.append(user_)

        return new_filter


class Users(AbstractBaseUser, PermissionsMixin):
    TYPE = (
        ('theme_admin', 'Administrador do tema',),
        ('theme_user', 'Usuário do tema',),
        ('partner', 'Parceiro',),
    )

    user_auth = models.ForeignKey('Users', verbose_name='Usuário de cadastro', help_text='Usuário que o cadastro',
                                  null=True, blank=True, related_name='user_insert')
    username = models.CharField(verbose_name='Username', help_text='Username do usuário relacionado', max_length=30,
                                unique=True, )
    email = models.CharField(verbose_name='E-mail', help_text='E-mail do usuário relacionado', max_length=255, )
    first_name = models.CharField(verbose_name='Nome', help_text='Nome do usuário relacionado',
                                  max_length=255, )
    last_name = models.CharField(verbose_name='Sobrenome', help_text='Sobrenome do usuário relacionado',
                                 max_length=255, )
    phone = models.CharField(verbose_name='Telefone', max_length=100, null=True, blank=True, )
    cell = models.CharField(verbose_name='Celular', max_length=100, null=True, blank=True, )
    institution = models.CharField(verbose_name='Instituição', max_length=255, null=True, blank=True, )
    departament = models.CharField(verbose_name='departamento', max_length=255, null=True, blank=True, )
    type = models.CharField(verbose_name='Tipo', help_text='Selecione o tipo de usuário', choices=TYPE,
                            max_length=20, )
    is_active = models.BooleanField(default=True, verbose_name='Ativo',
                                    help_text='Determina se este usuário deve ser tratado como ativo. Desmarque esta opção em vez de excluir contas.')
    is_staff = models.BooleanField(default=False, verbose_name='Membro da equipe',
                                   help_text='Determina se o usuário pode acessar o Administrador.')

    date_joined = models.DateTimeField('Data de cadastro', default=timezone.now)

    objects = UsersManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', ]

    def get_full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name)

    get_full_name.short_description = 'Nome completo'

    def get_short_name(self):
        return '{0}'.format(self.first_name)

    get_short_name.short_description = 'Nome'

    def __str__(self):
        return u"{0} {1}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class UsersPermissionManager(models.Manager):
    def add_permission_user(self, user, permission):
        item = self.model(
            user=user,
            permission=permission
        )

        item.save(using=self._db)
        return item


class UsersPermission(models.Model):
    user = models.ForeignKey(Users, verbose_name='Usuário', related_name='permissions')
    permission = models.ForeignKey(Permission, verbose_name='Permissão', )
    objects = UsersPermissionManager()

    def __unicode__(self):
        return '{0}'.format(self.user)

    class Meta:
        verbose_name = 'Permissão do usuário'
        verbose_name_plural = 'Permissões do usuário'


class UsersThemeManager(models.Manager):
    def add_theme_user(self, user, theme):
        item = self.model(
            user=user,
            theme=theme
        )

        item.save(using=self._db)
        return item


class UsersTheme(models.Model):
    user = models.ForeignKey(Users, verbose_name='Usuário', related_name='themes')
    theme = models.ForeignKey(Theme, verbose_name='Tema', )
    objects = UsersThemeManager()

    def __str__(self):
        return '{0}'.format(self.theme)

    class Meta:
        verbose_name = 'Tema do usuário'
        verbose_name_plural = 'Temas do usuário'


class UsersUFManager(models.Manager):
    def add_uf_user(self, user, uf):
        item = self.model(
            user=user,
            uf=uf
        )

        item.save(using=self._db)
        return item


class UsersUF(models.Model):
    user = models.ForeignKey(Users, verbose_name='Usuário', related_name='states')
    uf = models.ForeignKey(UF, verbose_name='UF', help_text='Selecione um estado que o usuário pertence', )
    objects = UsersUFManager()

    def __str__(self):
        return '{0}'.format(self.uf)

    class Meta:
        verbose_name = 'UF do usuário'
        verbose_name_plural = 'UFs do usuário'
