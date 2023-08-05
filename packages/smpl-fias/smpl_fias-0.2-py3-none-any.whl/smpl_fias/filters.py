
from django_filters import rest_framework as filters

from .models import *

__all__ = ['FIAS_ObjectFilter']


class FIAS_ObjectFilter(filters.FilterSet):

    class Meta:
        model = FIAS_Object
        fields = {
            'aoid': ['exact'],
            'level': ['exact'],
            'live_status': ['exact'],
            'parent_guid': ['exact']
        }

    search_by_name = filters.CharFilter(method='search_by_name_filter')

    def search_by_name_filter(self, queryset, name, value):
        if value:
            return queryset.extra(
                select={'range': 'similarity(%s, name)'},
                select_params=(value,),
                where=('similarity(%s, name) > 0.2',),
                params=(value,)
            ).order_by('-range')

        return queryset
