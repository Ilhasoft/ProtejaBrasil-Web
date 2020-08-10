from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from geoposition.forms import GeopositionField
from apps.protectionnetwork.models import Type, ProtectionNetwork
from apps.theme.models import Theme
from apps.uf.models import UF
from apps.user.models import Users
from sorl.thumbnail.fields import ImageField
from apps.violation.models import TypeViolation, TypeViolationInternationalization

__author__ = 'teehamaral'


class LoginUserForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Usuário',
                'required': '',
                'class': 'form-control',
            }
        ))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Senha',
                'required': '',
                'class': 'form-control',
            }
        ))

    def clean(self):
        if not authenticate(username=self.cleaned_data.get('username', ''),
                            password=self.cleaned_data.get('password', '')):
            raise ValidationError('Usuário ou senha incorreta.')


class AddUserForm(forms.ModelForm):
    TYPES = [
        ('theme_admin', 'Administrador do tema'),
        ('theme_user', 'Usuário do tema')
    ]

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Usado para entrar no sistema',
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nome',
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Sobrenome',
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'E-mail',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Senha',
                'required': '',
                'class': 'form-control'
            }
        ))
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmação da senha',
                'required': '',
                'class': 'form-control'
            }
        ))
    institution = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Instuição',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    departament = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Departamento',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    cell = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '(00) 9 0000-0000',
                'autocomplete': 'off',
                'class': 'form-control celular'
            }
        ))
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '(00) 9 0000-0000',
                'autocomplete': 'off',
                'class': 'form-control telefone'
            }
        ))
    type = forms.ChoiceField(
        required=False,
        choices=TYPES,
        widget=forms.RadioSelect()
    )
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput()
    )

    class Meta:
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'institution',
                  'departament', 'cell', 'phone', 'type', ]
        model = Users

    def clean(self):
        list_group = ('theme_admin', 'theme_user', u'')
        if not self.cleaned_data.get(u'type') in list_group:
            raise ValidationError('Selecione um tipo válido.')

        if self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password'):
            raise ValidationError('Senha e confirmação de senha não conferem')

        user_app = Users.objects.filter(username=self.cleaned_data.get(u'username'))
        if user_app.count() > 0:
            raise ValidationError('Este username já foi cadastrado anteriormente.')

        return self.cleaned_data


class EditUserForm(forms.ModelForm):
    TYPES = [
        ('theme_admin', 'Administrador do tema'),
        ('theme_user', 'Usuário do tema')
    ]

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nome',
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Sobrenome',
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'E-mail',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    institution = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Instuição',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    departament = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Departamento',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    cell = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '(00) 9 0000-0000',
                'autocomplete': 'off',
                'class': 'form-control celular'
            }
        ))
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '(00) 9 0000-0000',
                'autocomplete': 'off',
                'class': 'form-control telefone'
            }
        ))
    type = forms.ChoiceField(
        required=False,
        choices=TYPES,
        widget=forms.RadioSelect()
    )
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput()
    )

    class Meta:
        fields = ['first_name', 'last_name', 'email', 'is_active', 'institution',
                  'departament', 'cell', 'phone', 'type', ]
        model = Users


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Senha',
                'required': '',
                'class': 'form-control'
            }
        ))
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmação da senha',
                'required': '',
                'class': 'form-control'
            }
        ))

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password'):
            raise ValidationError('Senha e confirmação de senha não conferem')

        return self.cleaned_data


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Usuário cadastrado no sistema',
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))

    def clean(self):
        user = Users.objects.filter(username=self.cleaned_data.get('username'))
        if user.count() > 0:
            user = user[0]
            if not user.email:
                raise ValidationError(
                    'O usuário informado foi encontrado, mas não há um e-mail cadastrado para enviarmos a nova senha. Por favor, entre em contato com o administrador do sistema.')
        else:
            raise ValidationError('O usuário informado não consta em nossa base de dados.')

        return self.cleaned_data


class AddTypeProctetionNetworkForm(forms.ModelForm):
    color = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'class': "form-control color{hash:true, pickerFaceColor:'transparent', pickerFace:3, pickerBorder:0, pickerInsetColor:'black'}"
            }
        ))
    icon = ImageField(blank=True, null=True)

    class Meta:
        model = Type
        fields = ['color', 'icon']

    def clean(self):
        return self.cleaned_data


class AddTypeProctetionNetworkInternationalizationForm(forms.Form):
    name_pt = forms.CharField(
        required=True,
        label='Nome *',
        widget=forms.TextInput(
            attrs={
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    name_en = forms.CharField(
        required=False,
        label='Name',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    name_es = forms.CharField(
        required=False,
        label='Nombre',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))

    def clean(self):
        if not self.cleaned_data.get('name_pt'):
            raise ValidationError('Preencha os campos obrigatórios.')

        return self.cleaned_data


class AddProctetionNetworkForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        required=True,
        widget=forms.Select(
            attrs={
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ),
        queryset=Type.objects.all()
    )
    position = GeopositionField()
    zipcode = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control cep'
            }
        )
    )
    address = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    neighborhood = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    state = forms.ChoiceField(
        required=True,
        widget=forms.Select(
            attrs={
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    contact = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    phone1 = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control telefone'
            }
        )
    )
    phone2 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control telefone'
            }
        )
    )
    email = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    schedule = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AddProctetionNetworkForm, self).__init__(*args, **kwargs)
        states = user.states.all()
        choices = []
        choices.append(('', '---------'))

        for state in states:
            choices.append((state.uf_id, state.uf.title))

        self.fields['state'].choices = choices

    class Meta:
        model = ProtectionNetwork
        fields = ['type', 'position', 'zipcode', 'neighborhood', 'address', 'city', 'state', 'contact',
                  'phone1', 'phone2', 'email', 'schedule']

    def clean_state(self):
        state = get_object_or_404(UF, id=self.cleaned_data.get('state'))
        return state


class AddProctetionNetworkInternationalizationForm(forms.Form):
    name_pt = forms.CharField(
        required=True,
        label='Nome *',
        widget=forms.TextInput(
            attrs={
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    name_en = forms.CharField(
        required=False,
        label='Name',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    name_es = forms.CharField(
        required=False,
        label='Nombre',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))

    def clean(self):
        if not self.cleaned_data.get('name_pt'):
            raise ValidationError('Preencha os campos obrigatórios.')

        return self.cleaned_data


class AddTypeViolationForm(forms.ModelForm):
    theme = forms.ChoiceField(
        required=True,
        widget=forms.Select(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AddTypeViolationForm, self).__init__(*args, **kwargs)
        themes = user.themes.all()
        choices = []
        choices.append(('', '---------'))

        for theme in themes:
            choices.append((theme.theme_id, theme.theme.info.all().order_by('-language').first().title))

        self.fields['theme'].choices = choices

    class Meta:
        model = TypeViolation
        fields = ['theme']

    def clean_theme(self):
        if self.cleaned_data.get('theme'):
            return get_object_or_404(Theme, id=self.cleaned_data.get('theme'))


class AddTypeViolationInternationalizationForm(forms.Form):
    name_pt = forms.CharField(
        required=True,
        label='Nome *',
        widget=forms.TextInput(
            attrs={
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    name_en = forms.CharField(
        required=False,
        label='Name *',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    name_es = forms.CharField(
        required=False,
        label='Nombre *',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ))
    description_pt = forms.CharField(
        required=True,
        label='Descrição *',
        widget=forms.Textarea(
            attrs={
                'required': '',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    description_en = forms.CharField(
        required=False,
        label='Description *',
        widget=forms.Textarea(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    description_es = forms.CharField(
        required=False,
        label='Descripción *',
        widget=forms.Textarea(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    action_pt = forms.CharField(
        required=False,
        label='Ação',
        help_text='Insira a ação a ser tomada pelo usuário do aplicativo.',
        widget=forms.Textarea(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    action_en = forms.CharField(
        required=False,
        label='Action',
        help_text='Enter the action to be taken by the application user.',
        widget=forms.Textarea(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    action_es = forms.CharField(
        required=False,
        label='Acción',
        help_text='Introduzca la acción a tomar por el usuario de la aplicación.',
        widget=forms.Textarea(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )

    def clean(self):
        if not self.cleaned_data.get('name_pt') or not self.cleaned_data.get('description_pt'):
            raise ValidationError('Preencha os campos obrigatórios.')

        return self.cleaned_data


class ImportProtectionNetworks(forms.Form):
    file = forms.FileField(
        required=True,
        widget=forms.FileInput()
    )
