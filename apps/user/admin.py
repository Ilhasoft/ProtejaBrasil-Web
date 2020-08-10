# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from apps.user.models import UsersTheme, UsersUF, Users, UsersPermission


class UserThemeInline(admin.StackedInline):
    model = UsersTheme
    extra = 0


class UserUFInline(admin.StackedInline):
    model = UsersUF
    extra = 0


class UsersCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de senha', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u"As senhas não são iguais.")
        return password2

    def save(self, commit=True):
        user = super(UsersCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UsersChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Password',
                                         help_text="Não há nenhuma maneira de ver a senha do usuário, mas pode alterá-la usando <a href='password/'>este formulário</a>")

    class Meta:
        model = Users
        fields = (
            'username', 'password', 'first_name', 'last_name', 'email', 'phone', 'institution', 'departament', 'cell',
            'is_active', 'is_superuser',
        )

    def clean_password(self):
        return self.initial["password"]


class UsersAdmin(UserAdmin):
    form = UsersChangeForm
    add_form = UsersCreationForm

    inlines = [UserThemeInline, UserUFInline, ]
    list_display = ('username', 'get_full_name', 'email', 'is_active', 'is_superuser',)
    list_display_links = list_display
    list_filter = ('is_superuser', 'is_active', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        ('Nome', {'fields': ('first_name', 'last_name',)}),
        ('Instituição', {'fields': ('institution', 'departament',)}),
        ('Contato', {'fields': ('email', 'cell', 'phone',)}),
        ('Permissões', {'fields': ('is_superuser', 'is_staff', 'is_active', 'type',)}),
        ('Datas importantes', {'fields': ('date_joined', 'last_login',)}),
    )
    radio_fields = {'type': admin.VERTICAL}
    list_per_page = 30

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'first_name', 'last_name', 'email', 'phone', 'cell', 'institution', 'departament', 'type',
                'is_superuser', 'is_staff', 'password1', 'password2')
        }),
    )
    search_fields = ('username', 'first_name', 'email', 'institution',)
    ordering = ('first_name',)


class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission',)
    list_display_links = list_display
    list_per_page = 30
    list_filter = ('user', 'permission',)
    raw_id_fields = ('user',)
    search_fields = ('user__first_name', 'user__username',)


admin.site.register(Users, UsersAdmin)
admin.site.register(UsersPermission, UserPermissionAdmin)
