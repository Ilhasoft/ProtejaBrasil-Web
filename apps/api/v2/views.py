from decimal import *
import operator
import json

from rest_framework import permissions, decorators
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.authorization.models import Token
from apps.feedback.models import Feedback as Feedback_
from apps.protectionnetwork.models import Type, ProtectionNetwork, ThemeProtectionNetwork
from apps.api.v2.serializers import TypeProtectionNetworkSerializer, ProtectionNetworkSerializer, TypeViolationSerializer, FeedbackSerializer, ThemeSerializer
from apps.theme.models import Theme
from apps.uf.models import UF
from apps.utils.utils import getDestinationLatLong, getPathLength
from apps.violation.models import TypeViolation
from django.db.models import Q

DEFAULT_LANGUAGE = 'pt'


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def theme(request):
    '''
    All themes

    * **id** - the ID (int)
    * **title** - the NAME (string)
    * **icon** - the ICON (string)
    * **color** - the COLOR (string)
    * **description** - the DESCRIPTION (string)
    * **sondha_id** - the id used for SONDHA system (int)

    ##Exemple:

        GET /api/v2/themes/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            items = Theme.objects.all().order_by('order')
            results = []
            for item in items:
                try:
                    item.title = item.info.all().filter(language=lang).first().title
                    item.description = item.info.all().filter(language=lang).first().description
                except:
                    pass
                results.append(item)
            serializer = ThemeSerializer(results, many=True)
            return Response(serializer.data)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def theme_getone(request, theme_id):
    '''
    One theme based on ID parameter

    * **id** - the ID (int)
    * **title** - the NAME (string)
    * **icon** - the ICON (string)
    * **color** - the COLOR (string)
    * **description** - the DESCRIPTION (string)
    * **sondha_id** - the id used for SONDHA system (int)

    ##Exemple:

        GET /api/v2/themes/1/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            try:
                lang = request.GET.get('lang') or DEFAULT_LANGUAGE
                result = Theme.objects.get(id=theme_id)
                try:
                    result.title = result.info.all().filter(language=lang).first().title
                    result.description = result.info.all().filter(language=lang).first().description
                except:
                    pass
                serializer = ThemeSerializer(result, many=False)
                return Response(serializer.data)
            except:
                data = {'return': '404_NOT_FOUND'}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def typeprotectionnetwork(request):
    '''
    All types of protection network

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **color** - the COLOR (string)
    * **icon** - the URL IMAGE (string)

    ##Exemple:

        GET /api/v2/protection_network/types/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            items = Type.objects.all().order_by('name')
            results = []
            for item in items:
                try:
                    item.name = item.info.all().filter(language=lang).first().name
                except:
                    pass
                results.append(item)
            serializer = TypeProtectionNetworkSerializer(results, many=True)
            return Response(serializer.data)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def typeprotectionnetwork_getone(request, typeprotectionnetwork_id):
    '''
    One type of protection network

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **color** - the COLOR (string)
    * **icon** - the URL IMAGE (string)

    ##Exemple:

        GET /api/v2/protection_network/types/1/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query
    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            try:
                result = Type.objects.get(id=typeprotectionnetwork_id)
                try:
                    result.name = result.info.all().filter(language=lang).first().name
                    # result.lang = lang
                except:
                    pass
                serializer = TypeProtectionNetworkSerializer(result, many=False)
                return Response(serializer.data)
            except:
                data = {'return': '404_NOT_FOUND'}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def protectionnetwork(request):
    '''
    All protection networks

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **types** - the TYPES PROTECTION NETWORK (object)
    * **position** - the LAT and LONG (object)
    * **zipcode** - the ZIPCODE (string)
    * **neighborhood** - the NEIGHBORHOOD (string)
    * **address** - the ADDRESS (string)
    * **city** - the CITY (string)
    * **state** - the STATE (object)
    * **contact** - the CONTACT (string)
    * **phone1** - the NUMBER PHONE 1 (string)
    * **phone2** - the NUMBER PHONE 2 (string)
    * **email** - the EMAIL (string)
    * **schedule** - the SCHEDULE (string)
    * **themes** - the THEMES (array)
    * **operatingdays** - the OPERATING DAYS (array)

    ##Exemple:

        GET /api/v2/protection_network/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            items = ProtectionNetwork.objects.all().order_by('name')
            results = []
            for item in items:
                try:
                    item.name = item.info.all().filter(language=lang).first().name
                except:
                    pass
                results.append(item)
            serializer = ProtectionNetworkSerializer(results, many=True, context={'lang': lang})
            return Response(serializer.data)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def protectionnetwork_getone(request, protectionnetwork_id):
    '''
    One protection network based on ID parameter

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **types** - the TYPES PROTECTION NETWORK (object)
    * **position** - the LAT and LONG (object)
    * **zipcode** - the ZIPCODE (string)
    * **neighborhood** - the NEIGHBORHOOD (string)
    * **address** - the ADDRESS (string)
    * **city** - the CITY (string)
    * **state** - the STATE (object)
    * **contact** - the CONTACT (string)
    * **phone1** - the NUMBER PHONE 1 (string)
    * **phone2** - the NUMBER PHONE 2 (string)
    * **email** - the EMAIL (string)
    * **schedule** - the SCHEDULE (string)
    * **themes** - the THEMES (array)
    * **operatingdays** - the OPERATING DAYS (array)

    ##Exemple:

        GET /api/v2/protection_network/1/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            try:
                result = ProtectionNetwork.objects.get(id=protectionnetwork_id)
                try:
                    result.name = result.info.all().filter(language=lang).first().name
                except:
                    pass
                serializer = ProtectionNetworkSerializer(result, many=False, context={'lang': lang})
                return Response(serializer.data)
            except:
                data = {'return': '404_NOT_FOUND'}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def protectionnetwork_getbyname(request, name):
    '''
    30 protection networks based on name parameter

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **types** - the TYPES PROTECTION NETWORK (object)
    * **position** - the LAT and LONG (object)
    * **zipcode** - the ZIPCODE (string)
    * **neighborhood** - the NEIGHBORHOOD (string)
    * **address** - the ADDRESS (string)
    * **city** - the CITY (string)
    * **state** - the STATE (object)
    * **contact** - the CONTACT (string)
    * **phone1** - the NUMBER PHONE 1 (string)
    * **phone2** - the NUMBER PHONE 2 (string)
    * **email** - the EMAIL (string)
    * **schedule** - the SCHEDULE (string)
    * **themes** - the THEMES (array)
    * **operatingdays** - the OPERATING DAYS (array)

    ##Exemple:

        GET /api/v2/protection_network/name/test/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            try:
                items = ProtectionNetwork.objects.filter(Q(name__icontains=name) | Q(info__name__icontains=name)).order_by('name')[:30]
                results = []
                for item in items:
                    try:
                        item.name = item.info.all().filter(language=lang).first().name
                    except:
                        pass
                    results.append(item)
                serializer = ProtectionNetworkSerializer(results, many=True, context={'lang': lang})
                return Response(serializer.data)
            except:
                data = {'return': '404_NOT_FOUND'}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def protectionnetwork_getbynameandcoordenates(request, name, lat, long):
    '''
    30 protection networks based on name and position (lat, long) parameter

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **types** - the TYPES PROTECTION NETWORK (object)
    * **position** - the LAT and LONG (object)
    * **zipcode** - the ZIPCODE (string)
    * **neighborhood** - the NEIGHBORHOOD (string)
    * **address** - the ADDRESS (string)
    * **city** - the CITY (string)
    * **state** - the STATE (object)
    * **contact** - the CONTACT (string)
    * **phone1** - the NUMBER PHONE 1 (string)
    * **phone2** - the NUMBER PHONE 2 (string)
    * **email** - the EMAIL (string)
    * **schedule** - the SCHEDULE (string)
    * **themes** - the THEMES (array)
    * **operatingdays** - the OPERATING DAYS (array)

    ##Exemple:

        GET /api/v2/protection_network/name/test/position/-9.000,-36.0000/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: long
          paramType: path
          required: true
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            try:
                filter_lat = float(lat)
                filter_long = float(long)

                protectionnetworks = ProtectionNetwork.objects.filter(Q(name__icontains=name) | Q(info__name__icontains=name)).order_by(u'name')

                dict_protectionnetworks = {}
                if len(protectionnetworks) > 0:
                    for prtnet in protectionnetworks:
                        d = getPathLength(filter_lat, filter_long, float(prtnet.position.latitude),
                                          float(prtnet.position.longitude))
                        dict_protectionnetworks[prtnet.id] = d

                    order_dict = sorted(dict_protectionnetworks.items(), key=operator.itemgetter(1))
                    order_dict = order_dict[:30]

                    filter = []
                    for protecnet in order_dict:
                        getone_protectionnetwork = ProtectionNetwork.objects.get(id=protecnet[0])
                        filter.append(getone_protectionnetwork)

                    results = []
                    for item in filter:
                        try:
                            item.name = item.info.all().filter(language=lang).first().name
                        except:
                            pass
                        results.append(item)

                    serializer = ProtectionNetworkSerializer(results, many=True, context={'lang': lang})
                    data = serializer.data
                else:
                    data = []

                return Response(data)
            except:
                data = {'return': '404_NOT_FOUND'}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def protectionnetwork_getforstate(request, initials):
    '''
    All protection networks based on state parameter (Exemple param: AL, PE)

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **types** - the TYPES PROTECTION NETWORK (object)
    * **position** - the LAT and LONG (object)
    * **zipcode** - the ZIPCODE (string)
    * **neighborhood** - the NEIGHBORHOOD (string)
    * **address** - the ADDRESS (string)
    * **city** - the CITY (string)
    * **state** - the STATE (object)
    * **contact** - the CONTACT (string)
    * **phone1** - the NUMBER PHONE 1 (string)
    * **phone2** - the NUMBER PHONE 2 (string)
    * **email** - the EMAIL (string)
    * **schedule** - the SCHEDULE (string)
    * **themes** - the THEMES (array)
    * **operatingdays** - the OPERATING DAYS (array)

    ##Exemple:

        GET /api/v2/protection_network/state/AL/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            try:
                state = UF.objects.get(initials=initials)
                items = ProtectionNetwork.objects.filter(state=state).order_by('name')
                results = []
                for item in items:
                    try:
                        item.name = item.info.all().filter(language=lang).first().name
                    except:
                        pass
                    results.append(item)
                serializer = ProtectionNetworkSerializer(results, many=True, context={'lang': lang})
                return Response(serializer.data)
            except:
                data = {'return': '404_NOT_FOUND'}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def protectionnetwork_getfortheme(request, theme_id):
    '''
    All protection networks based on theme parameter

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **types** - the TYPES PROTECTION NETWORK (object)
    * **position** - the LAT and LONG (object)
    * **zipcode** - the ZIPCODE (string)
    * **neighborhood** - the NEIGHBORHOOD (string)
    * **address** - the ADDRESS (string)
    * **city** - the CITY (string)
    * **state** - the STATE (object)
    * **contact** - the CONTACT (string)
    * **phone1** - the NUMBER PHONE 1 (string)
    * **phone2** - the NUMBER PHONE 2 (string)
    * **email** - the EMAIL (string)
    * **schedule** - the SCHEDULE (string)
    * **themes** - the THEMES (array)
    * **operatingdays** - the OPERATING DAYS (array)

    ##Exemple:

        GET /api/v2/protection_network/theme/1/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            try:
                theme = Theme.objects.get(id=theme_id)
                protectionnetworks = ProtectionNetwork.objects.all()

                filter_protectionnetworks = []
                for pn in protectionnetworks:
                    themes_id = [t.theme_id for t in pn.themes.all()]
                    if theme.id in themes_id:
                        try:
                            pn.name = pn.info.all().filter(language=lang).first().name
                        except:
                            pass
                        filter_protectionnetworks.append(pn)

                serializer = ProtectionNetworkSerializer(filter_protectionnetworks, many=True, context={'lang': lang})
                return Response(serializer.data)
            except:
                data = {'return': '404_NOT_FOUND'}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def protectionnetwork_getforstateandtheme(request, initials, theme_id):
    '''
    All protection networks based on theme and state parameter

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **types** - the TYPES PROTECTION NETWORK (object)
    * **position** - the LAT and LONG (object)
    * **zipcode** - the ZIPCODE (string)
    * **neighborhood** - the NEIGHBORHOOD (string)
    * **address** - the ADDRESS (string)
    * **city** - the CITY (string)
    * **state** - the STATE (object)
    * **contact** - the CONTACT (string)
    * **phone1** - the NUMBER PHONE 1 (string)
    * **phone2** - the NUMBER PHONE 2 (string)
    * **email** - the EMAIL (string)
    * **schedule** - the SCHEDULE (string)
    * **themes** - the THEMES (array)
    * **operatingdays** - the OPERATING DAYS (array)

    ##Exemple:

        GET /api/v2/protection_network/state/AL/theme/1/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            try:
                state = UF.objects.get(initials=initials)
                theme = Theme.objects.get(id=theme_id)
                protectionnetworks = ProtectionNetwork.objects.filter(state=state).order_by(u'name')

                filter_protectionnetworks = []
                for pn in protectionnetworks:
                    themes_id = [t.theme_id for t in pn.themes.all()]
                    if theme.id in themes_id:
                        try:
                            pn.name = pn.info.all().filter(language=lang).first().name
                        except:
                            pass
                        filter_protectionnetworks.append(pn)

                serializer = ProtectionNetworkSerializer(filter_protectionnetworks, many=True, context={'lang': lang})
                return Response(serializer.data)
            except:
                data = {'return': '404_NOT_FOUND'}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def protectionnetwork_getfortype(request, type_id):
    '''
    All protection network based on type parameter

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **types** - the TYPES PROTECTION NETWORK (object)
    * **position** - the LAT and LONG (object)
    * **zipcode** - the ZIPCODE (string)
    * **neighborhood** - the NEIGHBORHOOD (string)
    * **address** - the ADDRESS (string)
    * **city** - the CITY (string)
    * **state** - the STATE (object)
    * **contact** - the CONTACT (string)
    * **phone1** - the NUMBER PHONE 1 (string)
    * **phone2** - the NUMBER PHONE 2 (string)
    * **email** - the EMAIL (string)
    * **schedule** - the SCHEDULE (string)
    * **themes** - the THEMES (array)
    * **operatingdays** - the OPERATING DAYS (array)

    ##Exemple:

        GET /api/v2/protection_network/type/1/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            try:
                violation_type = TypeViolation.objects.get(id=type_id)
                theme = Theme.objects.get(id=violation_type.theme.id)
                theme_protectionnetwork = ThemeProtectionNetwork.objects.filter(theme=theme)
                protectionnetworks = [pnt.protectionnetwork.id for pnt in theme_protectionnetwork]
                protectionnetworks = ProtectionNetwork.objects.filter(id__in=protectionnetworks).order_by('name')

                results = []
                for item in protectionnetworks:
                    try:
                        item.name = item.info.all().filter(language=lang).first().name
                    except:
                        pass
                    results.append(item)

                serializer = ProtectionNetworkSerializer(results, many=True, context={'lang': lang})
                return Response(serializer.data)
            except:
                data = {'return': '404_NOT_FOUND'}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def protectionnetwork_getfortypeandcoordenates(request, type_id, lat, long):
    '''
    Protection network nearest based on type and position (lat, long) parameter

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **types** - the TYPES PROTECTION NETWORK (object)
    * **position** - the LAT and LONG (object)
    * **zipcode** - the ZIPCODE (string)
    * **neighborhood** - the NEIGHBORHOOD (string)
    * **address** - the ADDRESS (string)
    * **city** - the CITY (string)
    * **state** - the STATE (object)
    * **contact** - the CONTACT (string)
    * **phone1** - the NUMBER PHONE 1 (string)
    * **phone2** - the NUMBER PHONE 2 (string)
    * **email** - the EMAIL (string)
    * **schedule** - the SCHEDULE (string)
    * **themes** - the THEMES (array)
    * **operatingdays** - the OPERATING DAYS (array)

    ##Exemple:

        GET /api/v2/protection_network/type/1/position/-39.0000,-75.0000/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: long
          paramType: path
          required: true
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        lang = request.GET.get('lang') or DEFAULT_LANGUAGE
        if request.method == "GET":
            try:
                filter_lat = float(lat)
                filter_long = float(long)

                violation_type = TypeViolation.objects.get(id=type_id)
                protectionnetwork_types = violation_type.get_types_id()
                protectionnetworks = ProtectionNetwork.objects.filter(type_id__in=protectionnetwork_types).order_by('name')

                dict_protectionnetworks = {}
                if len(protectionnetworks) > 0:
                    for prtnet in protectionnetworks:
                        d = getPathLength(filter_lat, filter_long, float(prtnet.position.latitude),
                                          float(prtnet.position.longitude))
                        dict_protectionnetworks[prtnet.id] = d

                    order_dict = sorted(dict_protectionnetworks.items(), key=operator.itemgetter(1))

                    result = ProtectionNetwork.objects.get(id=order_dict[0][0])

                    try:
                        result.name = result.info.all().filter(language=lang).first().name
                    except:
                        pass

                    serializer = ProtectionNetworkSerializer(result, many=False, context={'lang': lang})
                    data = serializer.data
                else:
                    data = []

                return Response(data)

            except Exception as e:
                data = {'return': e.args}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def protectionnetwork_getforthemeandcoordenates(request, theme_id, lat, long, distance):
    '''
    All protection networks based on parameters

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **types** - the TYPES PROTECTION NETWORK (object)
    * **position** - the LAT and LONG (object)
    * **zipcode** - the ZIPCODE (string)
    * **neighborhood** - the NEIGHBORHOOD (string)
    * **address** - the ADDRESS (string)
    * **city** - the CITY (string)
    * **state** - the STATE (object)
    * **contact** - the CONTACT (string)
    * **phone1** - the NUMBER PHONE 1 (string)
    * **phone2** - the NUMBER PHONE 2 (string)
    * **email** - the EMAIL (string)
    * **schedule** - the SCHEDULE (string)
    * **themes** - the THEMES (array)
    * **operatingdays** - the OPERATING DAYS (array)

    ##Exemple:

        GET /api/v2/protection_network/theme/1/position/-39.0000,-75.00000/radius/20000/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: long
          paramType: path
          required: true
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            try:
                from math import modf

                lat = float(lat)
                long = float(long)
                distance = int(distance)

                round_number = 1
                coordenates = getDestinationLatLong(lat, long, distance)
                d = getPathLength(lat, long, coordenates[0], coordenates[1])
                coords = []
                remainder, dist = modf((d / 1))
                coords.append([round(lat, round_number), round(long, round_number)])
                for i in range(1, int(dist)):
                    c = getDestinationLatLong(lat, long, i)
                    coords.append(c)
                coords.append([round(coordenates[0], round_number), round(coordenates[1], round_number)])

                theme = Theme.objects.get(id=theme_id)
                protectionnetworks = ProtectionNetwork.objects.all()

                filter_protectionnetworks = []

                for pn in protectionnetworks:
                    themes_id = [t.theme_id for t in pn.themes.all()]
                    if theme.id in themes_id:
                        try:
                            pn.name = pn.info.all().filter(language=lang).first().name
                        except:
                            pass
                        filter_protectionnetworks.append(pn)

                new_filter = []
                for new_pn in filter_protectionnetworks:
                    getcontext().rounding = ROUND_DOWN
                    position = [float(round(new_pn.position.latitude, round_number)),
                                float(round(new_pn.position.longitude, round_number))]

                    if position in coords:
                        new_filter.append(new_pn)

                serializer = ProtectionNetworkSerializer(new_filter, many=True, context={'lang': lang})
                return Response(serializer.data)
            except Exception as e:
                data = {'return': e.args}
                return Response(data=data, status=status.HTTP_502_BAD_GATEWAY)

    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


# TODO below

@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def typeviolation(request):
    '''
    All types of violation

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **description** - the DESCRIPTION (string)
    * **categories** - the CATEGORIES (object)
    * **theme** - the THEME (object)
    * **types** - the TYPES PROTECTION NETWORK (array)
    * **color** - the COLOR (string)
    * **icon** - the URL IMAGE (string)
    * **action** - the ACTION (strint)

    ##Exemple:

        GET /api/v2/violation_type/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            items = TypeViolation.objects.all().order_by('name')
            results = []
            for item in items:
                try:
                    item.name = item.info.all().filter(language=lang).first().name
                    item.description = item.info.all().filter(language=lang).first().description
                    item.action = item.info.all().filter(language=lang).first().action
                except:
                    pass
                results.append(item)
            serializer = TypeViolationSerializer(results, many=True, context={'lang': lang})
            return Response(serializer.data)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def typeviolation_getone(request, typeviolation_id):
    '''
    One type of violation based on type parameter

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **description** - the DESCRIPTION (string)
    * **categories** - the CATEGORIES (object)
    * **theme** - the THEME (object)
    * **types** - the TYPES PROTECTION NETWORK (array)
    * **color** - the COLOR (string)
    * **icon** - the URL IMAGE (string)
    * **action** - the ACTION (strint)

    ##Exemple:

        GET /api/v2/violation_type/1/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        lang = request.GET.get('lang') or DEFAULT_LANGUAGE
        if request.method == "GET":
            try:
                item = TypeViolation.objects.get(id=typeviolation_id)
                try:
                    item.name = item.info.all().filter(language=lang).first().name
                    item.description = item.info.all().filter(language=lang).first().description
                    item.action = item.info.all().filter(language=lang).first().action
                except:
                    pass
                serializer = TypeViolationSerializer(item, many=False, context={'lang': lang})
                return Response(serializer.data)
            except:
                data = {'return': '404_NOT_FOUND'}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def typeviolation_getfortheme(request, theme_id):
    '''
    All types of violation based on theme parameter

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **description** - the DESCRIPTION (string)
    * **categories** - the CATEGORIES (object)
    * **theme** - the THEME (object)
    * **types** - the TYPES PROTECTION NETWORK (array)
    * **color** - the COLOR (string)
    * **icon** - the URL IMAGE (string)
    * **action** - the ACTION (strint)

    ##Exemple:

        GET /api/v2/violation_type/theme/1/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        lang = request.GET.get('lang') or DEFAULT_LANGUAGE
        if request.method == "GET":
            try:
                theme = Theme.objects.get(id=theme_id)
                items = TypeViolation.objects.filter(theme=theme).order_by('name')
                results = []
                for item in items:
                    try:
                        item.name = item.info.all().filter(language=lang).first().name
                        item.description = item.info.all().filter(language=lang).first().description
                        item.action = item.info.all().filter(language=lang).first().action
                    except:
                        pass
                    results.append(item)
                serializer = TypeViolationSerializer(results, many=True, context={'lang': lang})
                return Response(serializer.data)
            except:
                data = {'return': '404_NOT_FOUND'}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def typeviolation_getfortype(request, typeprotectionnetwork_id):
    '''
    All types violation based on type of protection network parameter

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **description** - the DESCRIPTION (string)
    * **categories** - the CATEGORIES (object)
    * **theme** - the THEME (object)
    * **types** - the TYPES PROTECTION NETWORK (array)
    * **color** - the COLOR (string)
    * **icon** - the URL IMAGE (string)
    * **action** - the ACTION (strint)

    ##Exemple:

        GET /api/v2/violation_type/type/1/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            try:
                lang = request.GET.get('lang') or DEFAULT_LANGUAGE
                type = Type.objects.get(id=typeprotectionnetwork_id)
                typesviolation = TypeViolation.objects.all()

                filter_typesviolation = []
                for tv in typesviolation:
                    types_id = [t.typeprotectionnetwork_id for t in tv.typesprotectionnetwork.all()]
                    if type.id in types_id:
                        try:
                            tv.name = tv.info.all().filter(language=lang).first().name
                            tv.description = tv.info.all().filter(language=lang).first().description
                            tv.action = tv.info.all().filter(language=lang).first().action
                        except:
                            pass
                        filter_typesviolation.append(tv)

                serializer = TypeViolationSerializer(filter_typesviolation, many=True, context={'lang': lang})
                return Response(serializer.data)
            except:
                data = {'return': '404_NOT_FOUND'}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.AllowAny,))
def typeviolation_getforcategory(request, category):
    '''
    All types violation based on category parameter

    * **id** - the ID (int)
    * **name** - the NAME (string)
    * **description** - the DESCRIPTION (string)
    * **categories** - the CATEGORIES (object)
    * **theme** - the THEME (object)
    * **types** - the TYPES PROTECTION NETWORK (array)
    * **color** - the COLOR (string)
    * **icon** - the URL IMAGE (string)
    * **action** - the ACTION (strint)

    ##Values permitted in parameter
        InternetCrime
        Violation
        Accessibility


    ##Exemple:

        GET /api/v2/violation_type/category/Violation/
        HEADER {Authorization: token_authorization}

    ---
    parameters:
        - name: Authorization
          paramType: header
        - name: lang
          paramType: query

    '''

    try:
        token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except:
        token = None

    if token and token.is_active:
        if request.method == "GET":
            lang = request.GET.get('lang') or DEFAULT_LANGUAGE
            try:
                all_categories = ['Violation', 'InternetCrime', 'Accessibility']

                ERROR = []
                if category not in all_categories:
                    ERROR.append('Invalid category')

                if len(ERROR) == 0:
                    typesviolation = TypeViolation.objects.all()

                    filter_typesviolation = []
                    for tv in typesviolation:
                        categories_current = [ctv.category for ctv in tv.categories.all()]
                        if category in categories_current:
                            try:
                                tv.name = tv.info.all().filter(language=lang).first().name
                                tv.description = tv.info.all().filter(language=lang).first().description
                                tv.action = tv.info.all().filter(language=lang).first().action
                            except:
                                pass
                            filter_typesviolation.append(tv)

                    serializer = TypeViolationSerializer(filter_typesviolation, many=True, context={'lang': lang})
                    data = serializer.data
                else:
                    data = {'return': ERROR}

                return Response(data)
            except:
                data = {'return': '404_NOT_FOUND'}
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'return': '401_UNAUTHORIZED'}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


class Feedback(APIView):
    def post(self, request, format=None):
        '''
        Insert feedback \n
        Return feedback inserted

        * **id** - the ID (int)
        * **type** - the TYPE (string)
        * **name** - the NAME (string)
        * **email** - the E-MAIL (string)
        * **message** - the MESSAGE (string)
        * **platform** - the MESSAGE (string)
        * **version** - the MESSAGE (string)
        * **createdAt** - the creation date (datetime)

        ##Exemple:

            POST /api/v1/feedback/
            HEADER {Authorization: token_authorization}

            BODY EXEMPLE:
            {
                "type": "doubt",
                "name": "Your name",
                "email": "exemple@exemple.com",
                "message": "Your message",
                "platform": "android",
                "version": "1.1"
            }

        ##Values permitted in type field

            * "doubt"
            * "suggestion"
            * "criticism"
            * "compliment"

        ##Values permitted in platform field

            * "ios"
            * "android"

        ---
        parameters:
            - name: Authorization
              paramType: header
            - name: Body
              paramType: body

        '''

        try:
            token = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        except:
            token = None

        if token and token.is_active:
            body = json.loads(request.body.decode('utf-8', errors='ignore'))

            type = body.get('type')
            name = body.get('name')
            email = body.get('email')
            message = body.get('message')
            platform = body.get('platform')
            version = body.get('version')

            TYPE_PERM = ["doubt", "suggestion", "criticism", "compliment"]
            PLATFORM_PERM = ["ios", "android"]

            ERRORS = []
            if not type:
                ERRORS.append('type is required')

            if not name:
                ERRORS.append('name is required')

            if not email:
                ERRORS.append('email is required')

            if not message:
                ERRORS.append('message is required')

            if type not in TYPE_PERM:
                ERRORS.append('invalid type')

            if platform not in PLATFORM_PERM:
                ERRORS.append('invalid platform')

            if len(ERRORS) > 0:
                data = {'return': ERRORS}
                return_ = Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:

                new_obj = Feedback_.objects.add_feedback(
                    type=type,
                    name=name,
                    email=email,
                    message=message,
                    platform=platform,
                    version=version
                )

                try:
                    obj = Feedback_.objects.get(id=new_obj.pk)
                    serializer = FeedbackSerializer(obj, many=False)
                    return_ = Response(serializer.data)
                except:
                    data = {'return': 'ERROR_INSERT'}
                    return_ = Response(data, status=status.HTTP_400_BAD_REQUEST)

            return return_

        else:
            data = {'return': '401_UNAUTHORIZED'}
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    queryset = reports = Feedback_.objects.all().order_by('-id')
    serializer_class = FeedbackSerializer
