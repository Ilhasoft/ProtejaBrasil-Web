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
        fields = ('id', 'title', 'icon', 'color', 'description', 'sondha_id')


class TypeProtectionNetworkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    icon = serializers.ReadOnlyField(source='get_icon')

    class Meta:
        model = Type
        fields = ('id', 'name', 'color', 'icon',)


class ProtectionNetworkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    type = serializers.DictField(source='get_type')
    state = serializers.DictField(source='get_state')
    themes = serializers.ListField(source='get_themes', child=serializers.DictField())
    operatingdays = serializers.ListField(label='operatingdays', source='get_day', child=serializers.CharField())
    position = serializers.DictField(source='get_position')

    class Meta:
        model = ProtectionNetwork
        fields = (
            'id', 'name', 'type', 'position', 'zipcode', 'neighborhood', 'address', 'city', 'state',
            'contact', 'phone1', 'phone2', 'email', 'schedule', 'themes', 'operatingdays'
        )


class TypeViolationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    theme = serializers.DictField(source='get_theme')
    types = serializers.ListField(source='get_types', child=serializers.DictField())
    categories = serializers.ListField(source='get_categories', child=serializers.DictField())
    icon = serializers.ReadOnlyField(source='get_icon')

    class Meta:
        model = TypeViolation
        fields = (
            'id', 'name', 'description', 'theme', 'categories', 'types', 'color', 'icon', 'action'
        )


class FeedbackSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)

    class Meta:
        model = Feedback
        fields = (
            'id', 'type', 'name', 'email', 'message', 'platform', 'version', 'createdAt'
        )
