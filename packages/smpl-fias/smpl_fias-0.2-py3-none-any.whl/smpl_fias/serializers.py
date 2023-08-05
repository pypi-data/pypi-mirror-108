
from rest_framework import serializers

from .models import *

__all__ = [
    'FIAS_ObjectSerializer',
    'FIAS_FederalSubjectSerializer',
    'FIAS_LocalitySerializer',
    'FIAS_StreetSerializer'
]


class FIAS_ObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = FIAS_Object
        fields = '__all__'

    label = serializers.CharField(read_only=True)


class FIAS_FederalSubjectSerializer(FIAS_ObjectSerializer):

    class Meta:
        model = FIAS_FederalSubject
        fields = '__all__'


class FIAS_LocalitySerializer(FIAS_ObjectSerializer):

    class Meta:
        model = FIAS_Locality
        fields = '__all__'


class FIAS_StreetSerializer(FIAS_ObjectSerializer):

    class Meta:
        model = FIAS_Street
        fields = '__all__'

