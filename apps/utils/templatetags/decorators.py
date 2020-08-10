from django import template
from django.core.exceptions import PermissionDenied
from apps.permission.models import Permission
from apps.user.models import UsersPermission, Users

__author__ = 'teehamaral'
register = template.Library()

decorator_with_arguments = lambda decorator: lambda *args, **kwargs: lambda func: decorator(func, *args, **kwargs)


@decorator_with_arguments
def has_permission(function, permission_alias):
    def _function(request, *args, **kwargs):

        alias_verification = (
            'edit_user',
            'del_user',
            'change_password_user',
        )

        if permission_alias in alias_verification:
            url = request.META['PATH_INFO']
            objectid = url.split('/')
            indexOf = len(objectid) - 1
            objectid = objectid[indexOf - 1]
            user = Users.objects.filter(id=objectid)

            try:
                if user[0] == request.user:
                    return function(request, *args, **kwargs)
            except:
                raise PermissionDenied

        permission = Permission.objects.filter(alias=permission_alias)
        if permission.count() > 0:
            up = UsersPermission.objects.filter(user=request.user, permission=permission[0])
        else:
            up = []
        user_ = Users.objects.filter(id=request.user.id)

        if user_[0].type == 'theme_admin' or request.user.is_superuser:
            pass
        else:
            if len(up) == 0:
                raise PermissionDenied

        return function(request, *args, **kwargs)

    return _function
