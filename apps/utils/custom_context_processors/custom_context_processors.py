__author__ = 'teehamaral'


def user_auth(request):
    user_auth = request.user

    permissions_user_auth = []

    if user_auth.is_authenticated() and not user_auth.is_anonymous():
        permissions_user_auth = user_auth.permissions.all()
        permissions_user_auth = [pua.permission.alias for pua in permissions_user_auth]

    return {
        'user_auth': user_auth,
        'permissions_user_auth': permissions_user_auth
    }
