from rest_framework import serializers
from rest_framework.fields import CharField
from apps.feedback.models import Feedback
from apps.protectionnetwork.models import Type, ProtectionNetwork
from apps.theme.models import Theme
from apps.violation.models import TypeViolation

__author__ = 'teehamaral'


class ThemeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    icon = serializers.ReadOnlyField(source='get_icon')
    sondha_id = serializers.IntegerField(label='sondha_id', read_only=True)

    class Meta:
        model = Theme
        fields = ('id', 'title', 'icon', 'color', 'description', 'sondha_id',)


class TypeProtectionNetworkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    icon = serializers.ReadOnlyField(source='get_icon')

    class Meta:
        model = Type
        fields = ('id', 'name', 'color', 'icon',)


class ProtectionNetworkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    type = serializers.SerializerMethodField()
    state = serializers.DictField(source='get_state')
    themes = serializers.SerializerMethodField()
    operatingdays = serializers.SerializerMethodField()
    position = serializers.DictField(source='get_position')

    def get_operatingdays(self, obj):
        lang = self.context.get('lang')
        dict_days = {
            'pt': {
                'sunday': 'Domingo',
                'monday': 'Segunda-feira',
                'tuesday': 'Terça-feira',
                'wednesday': 'Quarta-feira',
                'thursday': 'Quinta-feira',
                'friday': 'Sexta-feira',
                'saturday': 'Sábado'
            },
            'en': {
                'sunday': 'Sunday',
                'monday': 'Monday',
                'tuesday': 'Tuesday',
                'wednesday': 'Wednesday',
                'thursday': 'Thursday',
                'friday': 'Friday',
                'saturday': 'Saturday'
            },
            'es': {
                'sunday': 'Domingo',
                'monday': 'Lunes',
                'tuesday': 'Martes',
                'wednesday': 'Miércoles',
                'thursday': 'Jueves',
                'friday': 'Viernes',
                'saturday': 'Sábado'
            }
        }
        if lang not in dict_days:
            lang = 'pt'
        week = dict_days.get(lang)
        days = []
        for item in obj.get_day():
            days.append(week[item.day])
        return days

    def get_type(self, obj):
        lang = self.context.get('lang')
        try:
            result = obj.get_type()
            try:
                result['name'] = obj.type.info.filter(language=lang).first().name
            except:
                pass

            type = result

        except:
            type = None

        return type

    def get_themes(self, obj):
        lang = self.context.get('lang')
        all = obj.themes.all()

        themes = []

        for theme in all:
            them = {}
            them['id'] = theme.theme.id

            try:
                title_internationalized = theme.theme.info.filter(language=lang).first().title
            except:
                title_internationalized = None

            them['name'] = title_internationalized if title_internationalized else theme.theme.title
            them['icon'] = theme.theme.get_icon()
            them['color'] = theme.theme.color

            try:
                description_internationalized = theme.theme.info.filter(language=lang).first().description
            except:
                description_internationalized = None

            them['description'] = description_internationalized if description_internationalized else theme.theme.description
            them['sondha_id'] = theme.theme.sondha_id
            themes.append(them)

        return themes

    class Meta:
        model = ProtectionNetwork
        fields = (
            'id', 'name', 'type', 'position', 'zipcode', 'neighborhood', 'address', 'city', 'state',
            'contact', 'phone1', 'phone2', 'email', 'schedule', 'themes', 'operatingdays',
        )


class TypeViolationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    theme = serializers.SerializerMethodField()
    types = serializers.SerializerMethodField()
    categories = serializers.ListField(source='get_categories', child=serializers.DictField())
    icon = serializers.ReadOnlyField(source='get_icon')

    def get_theme(self, obj):
        lang = self.context.get('lang')
        try:
            result = obj.get_theme()
            try:
                result['title'] = obj.theme.info.filter(language=lang).first().title
                result['description'] = obj.theme.info.filter(language=lang).first().description
            except:
                pass

            theme = result

        except:
            theme = None

        return theme

    def get_types(self, obj):
        lang = self.context.get('lang')
        all = obj.typesprotectionnetwork.all()

        types = []

        for type in all:
            typ = {}
            typ['id'] = type.typeprotectionnetwork.id

            try:
                title_internationalized = type.typeprotectionnetwork.info.filter(language=lang).first().name
            except:
                title_internationalized = None

            typ['name'] = title_internationalized if title_internationalized else type.typeprotectionnetwork.name
            typ['color'] = type.typeprotectionnetwork.color
            typ['icon'] = type.typeprotectionnetwork.get_icon()
            types.append(typ)

        return types

    class Meta:
        model = TypeViolation
        fields = (
            'id', 'name', 'description', 'theme', 'categories', 'types', 'color', 'icon', 'action',
        )


class FeedbackSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)

    class Meta:
        model = Feedback
        fields = (
            'id', 'type', 'name', 'email', 'message', 'platform', 'version', 'createdAt'
        )
