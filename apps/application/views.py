import datetime
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from geoposition import Geoposition
from apps.application.forms import LoginUserForm, AddUserForm, EditUserForm, ChangePasswordForm, ForgotPasswordForm, AddTypeProctetionNetworkForm, AddProctetionNetworkForm, AddTypeViolationForm, ImportProtectionNetworks, AddTypeViolationInternationalizationForm, AddTypeProctetionNetworkInternationalizationForm, AddProctetionNetworkInternationalizationForm
from django.contrib.auth import login as authlogin, authenticate
from django.contrib import messages
from apps.feedback.models import Feedback
from apps.importation.models import Import
from apps.log.models import Log
from apps.permission.models import Permission
from apps.protectionnetwork.models import Type, ProtectionNetwork, ThemeProtectionNetwork, OperatingDaysProtectionNetwork, TypeInternationalization, ProtectionNetworkInternationalization
from apps.theme.models import Theme
from apps.uf.models import UF
from apps.user.models import UsersPermission, Users, UsersTheme, UsersUF
from apps.utils.codgenarator import generator
from apps.utils.templatetags.decorators import has_permission
from apps.utils.utils import FilterGET
from apps.violation.models import TypeViolation, TypeProtectionNetwork, CategoryTypeViolation, TypeViolationInternationalization
from protejabrasil import settings

__author__ = 'teehamaral'


@csrf_protect
def login(request):
    if request.user.is_authenticated() and not request.user.is_anonymous():
        return redirect(reverse('app_dashboard'))

    if request.POST.get('next'):
        next_page = request.POST.get('next')
    else:
        next_page = reverse('app_dashboard')

    formlogin = LoginUserForm()

    if request.method == 'POST':
        formlogin = LoginUserForm(request.POST)
        if formlogin.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user.is_active:
                authlogin(request, user)
            else:
                messages.error(request, 'O usuário {0} está desativado.'.format(user))
                return redirect(reverse('app_login'))
            messages.success(request, 'Bem-vindo, {0}.'.format(user.get_full_name()))
            return redirect(next_page)
        else:
            messages.error(request, formlogin.non_field_errors())

    return render_to_response('application/login.html', RequestContext(request, {
        'form_login': formlogin
    }))


@csrf_protect
def forgotpassword(request):
    if request.user.is_authenticated() and not request.user.is_anonymous():
        return redirect(reverse('app_dashboard'))

    if request.method == 'POST':
        form = ForgotPasswordForm(data=request.POST)

        if form.is_valid():
            user = get_object_or_404(Users, username=request.POST.get('username'))
            new_password = generator(8)
            user.set_password(new_password)
            user.save()

            message = 'Olá, {0}.'.format(user.get_full_name())
            message += '\n \n'
            message += 'Segue a nova senha que geramos para você: {0}'.format(new_password)
            message += '\n \n'
            message += 'Você pode alterá-la posteriormente quando entrar no sistema.'

            send_mail(
                subject='Nova senha - Proteja Brasil',
                message=message,
                from_email=settings.EMAIL_ALIAS,
                recipient_list=[user.email],
                fail_silently=False
            )

            messages.success(request, 'Enviamos para o email cadastrado a sua nova senha.')
            return redirect(reverse('app_login'))
        else:
            messages.error(request, form.non_field_errors())

    else:
        form = ForgotPasswordForm()

    return render_to_response('application/forgot-password.html', RequestContext(request, {
        'form': form
    }))


@login_required(login_url='/')
def dashboard(request):
    filter = FilterGET(request, search_fields=[])
    search = filter.getQuerySet()

    # Violation types
    all_typeviolations = TypeViolation.objects.get_search(user=request.user, search=search)

    # Users
    all_users = Users.objects.get_search(user=request.user, search=search)
    users = all_users[:5]
    all_users = len(all_users)

    # Protection networks
    all_protectionnetworks = ProtectionNetwork.objects.get_search(user=request.user, search=search)
    protectionnetwork = all_protectionnetworks[:5]
    all_protectionnetworks = len(all_protectionnetworks)

    # Types protection network
    all_typeprotectionnetworks = Type.objects.get_search(search=search)
    typeprotectionnetwork = all_typeprotectionnetworks[:5]
    all_typeprotectionnetworks = len(all_typeprotectionnetworks)

    return render_to_response('application/dashboard.html', RequestContext(request, {
        'users': users,
        'users_count': all_users,
        'protectionnetwork': protectionnetwork,
        'protectionnetwork_count': all_protectionnetworks,
        'typeprotectionnetwork': typeprotectionnetwork,
        'typeprotectionnetwork_count': all_typeprotectionnetworks,
        'typeviolations': all_typeviolations[:5],
        'typeviolations_count': len(all_typeviolations)
    }))


@login_required(login_url='/')
@has_permission(permission_alias='list_user')
def users_list(request):
    users = FilterGET(request,
                      search_fields=['username', 'email', 'first_name', 'last_name', 'institution', 'departament'])
    search = users.getQuerySet()

    users = Users.objects.get_search(user=request.user, search=search)

    paginator = Paginator(users, 20)
    page = request.GET.get('pagina')

    if not page:
        page = 1

    esq = range(1, int(page))[-2:]
    dire = range(int(page), paginator.num_pages + 1)[:3]
    count_pages = list(esq) + list(dire)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.GET.get('q'):
        q = request.GET.get('q')
    else:
        q = ''

    return render_to_response('application/users/list.html', RequestContext(request, {
        'users': users,
        'count_pages': count_pages,
        'q': q
    }))


@login_required(login_url='/')
@has_permission(permission_alias='add_user')
@csrf_protect
def users_add(request):
    if request.method == 'POST':
        form_user = AddUserForm(data=request.POST)

        themes = request.POST.getlist('themes')
        ufs = request.POST.getlist('uf')

        if form_user.is_valid() and len(themes) > 0 and len(ufs) > 0:
            try:
                user = form_user.save(commit=False)
                user.set_password(request.POST.get('password'))
                if not request.POST.get('type'):
                    user.type = 'theme_user'
                user.user_auth = request.user
                user.save()

                permissions = request.POST.getlist('permissions')
                if len(permissions) > 0:
                    for perm in permissions:
                        permission = get_object_or_404(Permission, id=perm)
                        UsersPermission.objects.add_permission_user(user, permission)

                for them in themes:
                    theme = get_object_or_404(Theme, id=them)
                    UsersTheme.objects.add_theme_user(user, theme)

                for uf in ufs:
                    uf_ = get_object_or_404(UF, id=uf)
                    UsersUF.objects.add_uf_user(user, uf_)

                messages.success(request, 'Usuário cadastrado.')
                return redirect(reverse('app_userslist'))

            except Exception as e:
                messages.error(request, e)
        else:
            messages.error(request, form_user.non_field_errors())
            messages.error(request, 'Preencha todos os campos obrigatórios.')

    else:
        form_user = AddUserForm()

    permissions = Permission.objects.all()
    uf_user = request.user.states.all()
    themes_user = request.user.themes.all()

    return render_to_response('application/users/add.html', RequestContext(request, {
        'form_user': form_user,
        'permissions': permissions,
        'uf_user': uf_user,
        'themes_user': themes_user
    }))


@login_required(login_url='/')
@has_permission(permission_alias='edit_user')
@csrf_protect
def users_edit(request, id):
    current_user = get_object_or_404(Users, id=id)

    # Objects [permissions]
    permissions = Permission.objects.all()

    # Objects [uf, themes] user authenticated
    uf_user = request.user.states.all()
    themes_user = request.user.themes.all()

    # Objects [permissions, themes, uf] current user
    permissions_user = UsersPermission.objects.filter(user=current_user)
    themes_currente_user = UsersTheme.objects.filter(user=current_user)
    uf_current_user = UsersUF.objects.filter(user=current_user)

    # ID [permissions, themes, uf] current user
    user_permissions_id = [p.permission_id for p in permissions_user]
    user_themes_id = [t.theme_id for t in themes_currente_user]
    user_uf_id = [u.uf_id for u in uf_current_user]

    if request.method == 'POST':
        form_user = EditUserForm(data=request.POST, instance=current_user)

        themes = request.POST.getlist('themes')
        ufs = request.POST.getlist('uf')

        if form_user.is_valid() and len(themes) > 0 and len(ufs) > 0:
            try:
                user_ = form_user.save(commit=False)
                if not request.POST.get('type'):
                    user_.type = 'theme_user'
                user_.save()

                permissions = request.POST.getlist('permissions')

                if len(permissions) > 0:
                    for perm in permissions:
                        permission = get_object_or_404(Permission, id=perm)
                        if permission not in permissions_user:
                            UsersPermission.objects.add_permission_user(current_user, permission)

                    for p in permissions_user:
                        p.delete()

                for t in themes_currente_user:
                    t.delete()

                for u in uf_current_user:
                    u.delete()

                for them in themes:
                    theme = get_object_or_404(Theme, id=them)
                    UsersTheme.objects.add_theme_user(user_, theme)

                for uf in ufs:
                    uf_ = get_object_or_404(UF, id=uf)
                    UsersUF.objects.add_uf_user(user_, uf_)

                messages.success(request, 'Usuário editado.')
                return redirect(reverse('app_usersedit', args=[id]))
            except Exception as e:
                messages.error(request, e)
        else:
            messages.error(request, form_user.non_field_errors())
            messages.error(request, 'Preencha todos os campos obrigatórios.')

    else:
        form_user = EditUserForm(instance=current_user)

    return render_to_response('application/users/edit.html', RequestContext(request, {
        'form_user': form_user,
        'current_user': current_user,
        'permissions': permissions,
        'uf_user': uf_user,
        'themes_user': themes_user,
        'user_permissions_id': user_permissions_id,
        'user_themes_id': user_themes_id,
        'user_uf_id': user_uf_id,
    }))


@login_required(login_url='/')
@has_permission(permission_alias='del_user')
def users_del(request, id):
    user = get_object_or_404(Users, id=id)

    try:
        user.delete()
        messages.success(request, 'Usuário excluído.')
    except Exception as e:
        messages.error(request, e)

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/')
@has_permission(permission_alias='change_password_user')
@csrf_protect
def users_change_password(request, id):
    user = get_object_or_404(Users, id=id)

    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST)

        if form.is_valid():
            try:
                if user == request.user:
                    user = get_object_or_404(Users, id=request.user.id)
                user.set_password(request.POST.get('password'))
                user.save()
                messages.success(request, 'Senha alterada.')
                return redirect(reverse('app_userslist'))
            except Exception as e:
                messages.error(request, e)
        else:
            messages.error(request, form.non_field_errors())

    else:
        form = ChangePasswordForm()

    return render_to_response('application/users/change-password.html', RequestContext(request, {
        'form': form,
        'user': user
    }))


@login_required(login_url='/')
@has_permission(permission_alias='list_typeprotectionnetwork')
def typesprotectionnetwork_list(request):
    results = FilterGET(request, search_fields=['name'])
    search = results.getQuerySet()

    results = Type.objects.get_search(search=search)

    paginator = Paginator(results, 20)
    page = request.GET.get('pagina')

    if not page:
        page = 1

    esq = range(1, int(page))[-2:]
    dire = range(int(page), paginator.num_pages + 1)[:3]
    count_pages = list(esq) + list(dire)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    if request.GET.get('q'):
        q = request.GET.get('q')
    else:
        q = ''

    return render_to_response('application/typesprotectionnetwork/list.html', RequestContext(request, {
        'results': results,
        'count_pages': count_pages,
        'q': q
    }))


@login_required(login_url='/')
@has_permission(permission_alias='add_typeprotectionnetwork')
@csrf_protect
def typesprotectionnetwork_add(request):
    form = AddTypeProctetionNetworkForm()
    form_info = AddTypeProctetionNetworkInternationalizationForm()

    if request.method == 'POST':
        form = AddTypeProctetionNetworkForm(data=request.POST, files=request.FILES)
        form_info = AddTypeProctetionNetworkInternationalizationForm(data=request.POST)

        if form.is_valid() and form_info.is_valid():
            name_pt = form_info.cleaned_data.get('name_pt')
            name_en = form_info.cleaned_data.get('name_en')
            name_es = form_info.cleaned_data.get('name_es')

            typeprotection = form.save()
            typeprotection.name = name_pt
            typeprotection.save()

            TypeInternationalization.objects.create(typeprotection.id, 'pt', name_pt)

            if name_en:
                TypeInternationalization.objects.create(typeprotection.id, 'en', name_en)

            if name_es:
                TypeInternationalization.objects.create(typeprotection.id, 'es', name_es)

            messages.success(request, 'Tipo de rede de proteção cadastrado')
            return redirect(reverse('app_typesprotectionnetworklist'))
        else:
            messages.error(request, form.non_field_errors())

    return render_to_response('application/typesprotectionnetwork/add.html', RequestContext(request, {
        'form': form,
        'form_info': form_info
    }))


@login_required(login_url='/')
@has_permission(permission_alias='edit_typeprotectionnetwork')
@csrf_protect
def typesprotectionnetwork_edit(request, id):
    current_type = get_object_or_404(Type, id=id)

    form = AddTypeProctetionNetworkForm(instance=current_type)

    current_internationalization = {}
    for item in current_type.info.all():
        if item.language == 'pt':
            current_internationalization['name_pt'] = item.name
        elif item.language == 'en':
            current_internationalization['name_en'] = item.name
        elif item.language == 'es':
            current_internationalization['name_es'] = item.name

    form_info = AddTypeProctetionNetworkInternationalizationForm(initial=current_internationalization)

    if request.method == 'POST':
        form = AddTypeProctetionNetworkForm(instance=current_type, data=request.POST, files=request.FILES)
        form_info = AddTypeProctetionNetworkInternationalizationForm(data=request.POST)

        if form.is_valid() and form_info.is_valid():
            name_pt = form_info.cleaned_data.get('name_pt')
            name_en = form_info.cleaned_data.get('name_en')
            name_es = form_info.cleaned_data.get('name_es')

            typeprotection = form.save()
            typeprotection.name = name_pt
            typeprotection.save()

            info_pt = current_type.info.filter(language='pt').first()
            info_pt.name = name_pt
            info_pt.save()

            info_en = current_type.info.filter(language='en').first()
            if info_en and name_en:
                info_en.name = name_en
                info_en.save()
            elif name_en:
                TypeInternationalization.objects.create(typeprotection.id, 'en', name_en)
            else:
                try:
                    info_en.delete()
                except:
                    pass

            info_es = current_type.info.filter(language='es').first()
            if info_es and name_es:
                info_es.name = name_es
                info_es.save()
            elif name_es:
                TypeInternationalization.objects.create(typeprotection.id, 'es', name_es)
            else:
                try:
                    info_es.delete()
                except:
                    pass

            messages.success(request, 'Tipo de rede de proteção editado')
            return redirect(reverse('app_typesprotectionnetworkedit', args=[id]))
        else:
            messages.error(request, form.non_field_errors())

    return render_to_response('application/typesprotectionnetwork/edit.html', RequestContext(request, {
        'form': form,
        'form_info': form_info,
        'current_type': current_type
    }))


@login_required(login_url='/')
@has_permission(permission_alias='del_typeprotectionnetwork')
@csrf_protect
def typesprotectionnetwork_del(request, id):
    current_type = get_object_or_404(Type, id=id)
    try:
        current_type.delete()
        messages.success(request, 'Tipo de rede de proteção excluído')
    except Exception as e:
        messages.error(request, e)

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/')
@has_permission(permission_alias='list_protectionnetwork')
def protectionnetwork_list(request):
    results = FilterGET(request, search_fields=['name', 'city', 'state__initials', 'state__title'])
    search = results.getQuerySet()

    results = ProtectionNetwork.objects.get_search(user=request.user, search=search)

    paginator = Paginator(results, 20)
    page = request.GET.get('pagina')

    if not page:
        page = 1

    esq = range(1, int(page))[-2:]
    dire = range(int(page), paginator.num_pages + 1)[:3]
    count_pages = list(esq) + list(dire)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    if request.GET.get('q'):
        q = request.GET.get('q')
    else:
        q = ''

    return render_to_response('application/protectionnetwork/list.html', RequestContext(request, {
        'results': results,
        'count_pages': count_pages,
        'q': q
    }))


@login_required(login_url='/')
@has_permission(permission_alias='add_protectionnetwork')
def protectionnetwork_add(request):
    form = AddProctetionNetworkForm(user=request.user)
    form_info = AddProctetionNetworkInternationalizationForm()

    themes = request.user.themes.all()

    days = (
        ('sunday', 'Domingo'),
        ('monday', 'Segunda-feira'),
        ('tuesday', 'Terça-feira'),
        ('wednesday', 'Quarta-feira'),
        ('thursday', 'Quinta-feira'),
        ('friday', 'Sexta-feira'),
        ('saturday', 'Sábado'),
    )

    if request.method == 'POST':
        form = AddProctetionNetworkForm(user=request.user, data=request.POST)
        form_info = AddProctetionNetworkInternationalizationForm(data=request.POST)

        post_themes = request.POST.getlist('themes')
        post_days = request.POST.getlist('days')

        if form.is_valid() and len(post_themes) > 0 and len(post_days) > 0 and form_info.is_valid():
            name_pt = form_info.cleaned_data.get('name_pt')
            name_en = form_info.cleaned_data.get('name_en')
            name_es = form_info.cleaned_data.get('name_es')

            protectionnetwork = form.save()
            protectionnetwork.name = name_pt
            protectionnetwork.save()

            ProtectionNetworkInternationalization.objects.create(protectionnetwork.id, 'pt', name_pt)

            if name_en:
                ProtectionNetworkInternationalization.objects.create(protectionnetwork.id, 'en', name_en)

            if name_es:
                ProtectionNetworkInternationalization.objects.create(protectionnetwork.id, 'es', name_es)

            for them in post_themes:
                theme = get_object_or_404(Theme, id=them)

                ThemeProtectionNetwork.objects.add_theme_protectionnetwork(protectionnetwork, theme)

            for day in post_days:
                OperatingDaysProtectionNetwork.objects.add_operatingdays_protectionnetwork(protectionnetwork, day)

            messages.success(request, 'Rede de proteção cadastrada')
            return redirect(reverse('app_protectionnetworklist'))
        else:
            messages.error(request, 'Preencha todos os campos obrigatórios.')

    return render_to_response('application/protectionnetwork/add.html', RequestContext(request, {
        'form': form,
        'form_info': form_info,
        'themes': themes,
        'days': days
    }))


@login_required(login_url='/')
@has_permission(permission_alias='edit_protectionnetwork')
@csrf_protect
def protectionnetwork_edit(request, id):
    current_protectionnetwork = get_object_or_404(ProtectionNetwork, id=id)

    current_internationalization = {}
    for item in current_protectionnetwork.info.all():
        if item.language == 'pt':
            current_internationalization['name_pt'] = item.name
        elif item.language == 'en':
            current_internationalization['name_en'] = item.name
        elif item.language == 'es':
            current_internationalization['name_es'] = item.name

    themes = request.user.themes.all()

    days = (
        ('sunday', 'Domingo'),
        ('monday', 'Segunda-feira'),
        ('tuesday', 'Terça-feira'),
        ('wednesday', 'Quarta-feira'),
        ('thursday', 'Quinta-feira'),
        ('friday', 'Sexta-feira'),
        ('saturday', 'Sábado'),
    )

    current_protectionnetwork_days = current_protectionnetwork.operatingdays.all()
    current_protectionnetwork_days_id = [opd.day for opd in current_protectionnetwork_days]

    current_protectionnetwork_themes = current_protectionnetwork.themes.all()
    current_protectionnetwork_themes_id = [t.theme_id for t in current_protectionnetwork_themes]

    form = AddProctetionNetworkForm(user=request.user, instance=current_protectionnetwork)
    form_info = AddProctetionNetworkInternationalizationForm(initial=current_internationalization)

    if request.method == 'POST':
        form = AddProctetionNetworkForm(user=request.user, instance=current_protectionnetwork, data=request.POST)
        form_info = AddProctetionNetworkInternationalizationForm(data=request.POST)

        post_themes = request.POST.getlist('themes')
        post_days = request.POST.getlist('days')

        if form.is_valid() and len(post_themes) > 0 and len(post_days) > 0 and form_info.is_valid():
            name_pt = form_info.cleaned_data.get('name_pt')
            name_en = form_info.cleaned_data.get('name_en')
            name_es = form_info.cleaned_data.get('name_es')

            protectionnetwork = form.save()
            protectionnetwork.name = name_pt
            protectionnetwork.save()

            info_pt = current_protectionnetwork.info.filter(language='pt').first()
            info_pt.name = name_pt
            info_pt.save()

            info_en = current_protectionnetwork.info.filter(language='en').first()
            if info_en and name_en:
                info_en.name = name_en
                info_en.save()
            elif name_en:
                ProtectionNetworkInternationalization.objects.create(protectionnetwork.id, 'en', name_en)
            else:
                try:
                    info_en.delete()
                except:
                    pass

            info_es = current_protectionnetwork.info.filter(language='es').first()
            if info_es and name_es:
                info_es.name = name_es
                info_es.save()
            elif name_es:
                ProtectionNetworkInternationalization.objects.create(protectionnetwork.id, 'es', name_es)
            else:
                try:
                    info_es.delete()
                except:
                    pass

            for them in post_themes:
                theme = get_object_or_404(Theme, id=them)
                ThemeProtectionNetwork.objects.add_theme_protectionnetwork(protectionnetwork, theme)

            for day in post_days:
                OperatingDaysProtectionNetwork.objects.add_operatingdays_protectionnetwork(protectionnetwork, day)

            for t in current_protectionnetwork_themes:
                t.delete()

            for opd in current_protectionnetwork_days:
                opd.delete()

            messages.success(request, 'Rede de proteção editada')
            return redirect(reverse('app_protectionnetworkedit', args=[id]))
        else:
            messages.error(request, 'Preencha todos os campos obrigatórios.')

    return render_to_response('application/protectionnetwork/edit.html', RequestContext(request, {
        'form': form,
        'form_info': form_info,
        'current_protectionnetwork': current_protectionnetwork,
        'current_protectionnetwork_days': current_protectionnetwork_days_id,
        'current_protectionnetwork_themes_id': current_protectionnetwork_themes_id,
        'themes': themes,
        'days': days
    }))


@login_required(login_url='/')
@has_permission(permission_alias='del_protectionnetwork')
@csrf_protect
def protectionnetwork_del(request, id):
    current_protectionnetwork = get_object_or_404(ProtectionNetwork, id=id)
    try:
        current_protectionnetwork.delete()
        messages.success(request, 'Rede de proteção excluída')
    except Exception as e:
        messages.error(request, e)

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/')
@has_permission(permission_alias='list_typeviolation')
def typesviolation_list(request):
    results = FilterGET(request, search_fields=['name', 'description', 'action'])
    search = results.getQuerySet()

    results = TypeViolation.objects.get_search(user=request.user, search=search)

    paginator = Paginator(results, 20)
    page = request.GET.get('pagina')

    if not page:
        page = 1

    esq = range(1, int(page))[-2:]
    dire = range(int(page), paginator.num_pages + 1)[:3]
    count_pages = list(esq) + list(dire)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    if request.GET.get('q'):
        q = request.GET.get('q')
    else:
        q = ''

    return render_to_response('application/typesviolation/list.html', RequestContext(request, {
        'results': results,
        'count_pages': count_pages,
        'q': q
    }))


@login_required(login_url='/')
@has_permission(permission_alias='edit_typeviolation')
def typesviolation_add(request):
    form = AddTypeViolationForm(user=request.user)
    form_info = AddTypeViolationInternationalizationForm()

    types_protectionnetwork = FilterGET(request, search_fields=[])
    search = types_protectionnetwork.getQuerySet()
    types_protectionnetwork = Type.objects.get_search(search=search)

    categories_typeviolation = (
        ('Violation', 'Violação'),
        ('InternetCrime', 'Crime na internet'),
        ('Accessibility', 'Acessibilidade'),
    )

    if request.method == 'POST':
        form = AddTypeViolationForm(user=request.user, data=request.POST)
        form_info = AddTypeViolationInternationalizationForm(data=request.POST)

        post_typesprotectionnetwork = request.POST.getlist('typesprotectionnetwork')
        post_categoriestypeviolation = request.POST.getlist('categories_typeviolation')

        if len(post_categoriestypeviolation) == 1 and 'InternetCrime' in post_categoriestypeviolation:
            form.fields['theme'].required = False

        if form.is_valid() and len(post_typesprotectionnetwork) > 0 and form_info.is_valid():
            name_pt = form_info.cleaned_data.get('name_pt')
            name_en = form_info.cleaned_data.get('name_en')
            name_es = form_info.cleaned_data.get('name_es')
            description_pt = form_info.cleaned_data.get('description_pt')
            description_en = form_info.cleaned_data.get('description_en')
            description_es = form_info.cleaned_data.get('description_es')
            action_pt = form_info.cleaned_data.get('action_pt')
            action_en = form_info.cleaned_data.get('action_en')
            action_es = form_info.cleaned_data.get('action_es')

            typeviolation = form.save()
            typeviolation.name = name_pt
            typeviolation.description = description_pt
            typeviolation.action = action_pt
            typeviolation.save()

            for tpn in post_typesprotectionnetwork:
                type = get_object_or_404(Type, id=tpn)
                TypeProtectionNetwork.objects.add_type_protectionnetwork(typeviolation, type)

            for cvt in post_categoriestypeviolation:
                CategoryTypeViolation.objects.add_category_typeviolation(typeviolation, cvt)

            TypeViolationInternationalization.objects.create(typeviolation.id, 'pt', name_pt, description_pt, action_pt)

            if name_en and description_en:
                TypeViolationInternationalization.objects.create(typeviolation.id, 'en', name_en, description_en, action_en)

            if name_es and description_es:
                TypeViolationInternationalization.objects.create(typeviolation.id, 'es', name_es, description_es, action_es)

            messages.success(request, 'Tipo de violação cadastrado')
            return redirect(reverse('app_typesviolationlist'))
        else:
            messages.error(request, form.non_field_errors())
            messages.error(request, 'Preencha todos os campos obrigatórios')

    return render_to_response('application/typesviolation/add.html', RequestContext(request, {
        'form': form,
        'types_protectionnetwork': types_protectionnetwork,
        'categories_typeviolation': categories_typeviolation,
        'form_info': form_info
    }))


@login_required(login_url='/')
@has_permission(permission_alias='edit_typeviolation')
@csrf_protect
def typesviolation_edit(request, id):
    current = get_object_or_404(TypeViolation, id=id)

    current_internationalization = {}
    for item in current.info.all():
        if item.language == 'pt':
            current_internationalization['name_pt'] = item.name
            current_internationalization['description_pt'] = item.description
            current_internationalization['action_pt'] = item.action
        elif item.language == 'en':
            current_internationalization['name_en'] = item.name
            current_internationalization['description_en'] = item.description
            current_internationalization['action_en'] = item.action
        elif item.language == 'es':
            current_internationalization['name_es'] = item.name
            current_internationalization['description_es'] = item.description
            current_internationalization['action_es'] = item.action

    types_protectionnetwork = FilterGET(request, search_fields=[])
    search = types_protectionnetwork.getQuerySet()
    types_protectionnetwork = Type.objects.get_search(search=search)

    current_typesprotectionnetwork = current.typesprotectionnetwork.all()
    current_typesprotectionnetwork_id = [tpn.typeprotectionnetwork_id for tpn in current_typesprotectionnetwork]

    current_categoriesviolationtype = current.categories.all()
    current_categoriesviolationtype_id = [cvt.category for cvt in current_categoriesviolationtype]

    form = AddTypeViolationForm(user=request.user, instance=current)
    form_info = AddTypeViolationInternationalizationForm(initial=current_internationalization)

    categories_typeviolation = (
        ('Violation', 'Violação'),
        ('InternetCrime', 'Crime na internet'),
        ('Accessibility', 'Acessibilidade'),
    )

    if request.method == 'POST':
        form = AddTypeViolationForm(user=request.user, instance=current, data=request.POST)
        form_info = AddTypeViolationInternationalizationForm(data=request.POST)

        post_typesprotectionnetwork = request.POST.getlist('typesprotectionnetwork')
        post_categoriestypeviolation = request.POST.getlist('categories_typeviolation')

        if len(post_categoriestypeviolation) == 1 and 'InternetCrime' in post_categoriestypeviolation:
            form.fields['theme'].required = False

        if form.is_valid() and len(post_typesprotectionnetwork) > 0 and form_info.is_valid():
            name_pt = form_info.cleaned_data.get('name_pt')
            name_en = form_info.cleaned_data.get('name_en')
            name_es = form_info.cleaned_data.get('name_es')
            description_pt = form_info.cleaned_data.get('description_pt')
            description_en = form_info.cleaned_data.get('description_en')
            description_es = form_info.cleaned_data.get('description_es')
            action_pt = form_info.cleaned_data.get('action_pt')
            action_en = form_info.cleaned_data.get('action_en')
            action_es = form_info.cleaned_data.get('action_es')

            typeviolation = form.save()
            typeviolation.name = name_pt
            typeviolation.description = description_pt
            typeviolation.action = action_pt
            typeviolation.save()

            for tpn in post_typesprotectionnetwork:
                type = get_object_or_404(Type, id=tpn)
                TypeProtectionNetwork.objects.add_type_protectionnetwork(typeviolation, type)

            for ctpn in current_typesprotectionnetwork:
                ctpn.delete()

            for cvt in post_categoriestypeviolation:
                CategoryTypeViolation.objects.add_category_typeviolation(typeviolation, cvt)

            for ccvt in current_categoriesviolationtype:
                ccvt.delete()

            # Portuguese
            info_pt = current.info.filter(language='pt').first()
            info_pt.name = name_pt if name_pt else info_pt.name
            info_pt.description = description_pt if description_pt else info_pt.description
            info_pt.action = action_pt
            info_pt.save()

            # English
            info_en = current.info.filter(language='en').first()
            if info_en and (name_en or description_en):
                info_en.name = name_en if name_en else info_en.name
                info_en.description = description_en if description_en else info_en.description
                info_en.action = action_en
                info_en.save()
            elif name_en and description_en:
                TypeViolationInternationalization.objects.create(current.id, 'en', name_en, description_en, action_en)
            else:
                try:
                    info_en.delete()
                except:
                    pass

            # Spanish
            info_es = current.info.filter(language='es').first()
            if info_es and (name_es or description_es):
                info_es.name = name_es if name_es else info_es.name
                info_es.description = description_es if description_es else info_es.description
                info_es.action = action_es
                info_es.save()
            elif name_es and description_es:
                TypeViolationInternationalization.objects.create(current.id, 'es', name_es, description_es, action_es)
            else:
                try:
                    info_es.delete()
                except:
                    pass

            messages.success(request, 'Tipo de violação editado')
            return redirect(reverse('app_typesviolationedit', args=[id]))

        else:
            messages.error(request, form.non_field_errors())
            messages.error(request, 'Preencha todos os campos obrigatórios.')

    return render_to_response('application/typesviolation/edit.html', RequestContext(request, {
        'form': form,
        'current': current,
        'current_typesprotectionnetwork_id': current_typesprotectionnetwork_id,
        'types_protectionnetwork': types_protectionnetwork,
        'categories_typeviolation': categories_typeviolation,
        'current_categoriesviolationtype_id': current_categoriesviolationtype_id,
        'form_info': form_info
    }))


@login_required(login_url='/')
@has_permission(permission_alias='del_typeviolation')
@csrf_protect
def typesviolation_del(request, id):
    current = get_object_or_404(TypeViolation, id=id)
    try:
        current.delete()
        messages.success(request, 'Tipo de violação excluído')
    except Exception as e:
        messages.error(request, e)

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/')
@csrf_protect
def import_protectionnetworks(request):
    if request.user.is_superuser:
        form = ImportProtectionNetworks()
        if request.method == 'POST':
            form = ImportProtectionNetworks(data=request.POST, files=request.FILES)
            if form.is_valid():
                importation = Import.objects.add_import(file=request.FILES.get('file'))
                importation.save()
                f = open('{0}/{1}'.format(settings.MEDIA_ROOT, importation.file), 'r', encoding='utf-8',
                         errors='ignore')

                for line in f:
                    line = line.split(';')

                    try:
                        type_ = line[1]
                        if type_ == '14':
                            type_ = '1'
                        type_ = Type.objects.get(id=type_)
                    except:
                        type_ = None

                    try:
                        position = Geoposition(line[2], line[3])
                    except:
                        position = None

                    address = '{0}'.format(line[5])
                    neighborhood = '{0}'.format(line[6])
                    zipcode = '{0}'.format(line[7].replace('.', ''))
                    city = '{0}'.format(line[8])

                    try:
                        state = UF.objects.get(initials=line[9])
                    except:
                        state = None

                    name = '{0}'.format(line[10])
                    contact = '{0}'.format(line[11])
                    phone1 = '{0}'.format(line[12])
                    phone2 = '{0}'.format(line[13])
                    email = '{0}'.format(line[14])

                    try:
                        protectionnetwork = ProtectionNetwork.objects.add_protectionnetwork(
                            type=type_,
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
                        theme = Theme.objects.get(id=2)
                        ThemeProtectionNetwork.objects.add_theme_protectionnetwork(protectionnetwork, theme)
                    except:
                        pass

                f.close()

            messages.success(request, 'Dados importados')
            return redirect(request.META['HTTP_REFERER'])

        return render_to_response('application/importation/import.html', RequestContext(request, {
            'form': form
        }))

    else:
        raise PermissionDenied


@login_required(login_url='/')
@has_permission(permission_alias='list_feedback')
def feedback(request):
    TYPES = (
        ('doubt', 'Dúvida',),
        ('suggestion', 'Sugestão',),
        ('criticism', 'Crítica',),
        ('compliment', 'Elogio',),
    )

    PLATFORM = (
        ('ios', 'iOS',),
        ('android', 'Android',),
    )

    STATUS = (
        ('pending', 'Pendente',),
        ('resolved', 'Resolvido',),
    )

    results = FilterGET(request, search_fields=['id', 'name', 'email', 'platform', 'status'])
    search = results.getQuerySet()

    results = Feedback.objects.get_search(search=search)

    date_from = request.GET.get('from') or ''
    date_to = request.GET.get('to') or ''
    type_ = request.GET.get('type') or 'all'
    platform_ = request.GET.get('platform') or 'all'
    status_ = request.GET.get('status') or 'all'

    template_date_to = date_to
    template_date_from = date_from
    template_type = type_
    template_platform = platform_
    template_status = status_

    if date_from and date_from != '':
        date_from = datetime.datetime.strptime(date_from, '%d/%m/%Y').isoformat()
        results = results.filter(createdAt__gte=date_from)

    if date_to and date_to != '':
        date_to = datetime.datetime.strptime(date_to, '%d/%m/%Y').isoformat()
        date_to = date_to.replace('T00:00:00', 'T23:59:00')
        results = results.filter(createdAt__lte=date_to)

    if type_ and type_ != 'all':
        results = results.filter(type=type_)

    if platform_ and platform_ != 'all':
        results = results.filter(platform=platform_)

    if status_ and status_ != 'all':
        results = results.filter(status=status_)

    paginator = Paginator(results, 20)
    page = request.GET.get('pagina')

    if not page:
        page = 1

    esq = range(1, int(page))[-2:]
    dire = range(int(page), paginator.num_pages + 1)[:3]
    count_pages = list(esq) + list(dire)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render_to_response('application/feedback/list.html', RequestContext(request, {
        'types': TYPES,
        'results': results,
        'type': template_type,
        'date_to': template_date_to,
        'date_from': template_date_from,
        'count_pages': count_pages,
        'platforms': PLATFORM,
        'platform': template_platform,
        'all_status': STATUS,
        'status': template_status,
    }))


@login_required(login_url='/')
@has_permission(permission_alias='list_feedback')
def feedback_as_resolved(request, id):
    feedback = get_object_or_404(Feedback, id=id)

    try:
        feedback.status = 'resolved'
        feedback.save()
        messages.success(request, 'Opinião marcada como resolvida')
    except Exception as e:
        messages.error(request, 'A opinião não foi marcada como resolvida. Por favor, verifique o log.')
        Log.objects.create_log(identifier='feedback_mark_resolved', description=e)

    return redirect(request.META.get('HTTP_REFERER'))
