
from rest_framework.viewsets import ReadOnlyModelViewSet
from smpl_drf.pagination import Pagination

from .models import *
from .serializers import *
from .filters import *


class FIAS_ObjectView(ReadOnlyModelViewSet):
    queryset = FIAS_Object.objects.all()
    filterset_class = FIAS_ObjectFilter
    pagination_class = Pagination


class FIAS_FederalSubjectView(FIAS_ObjectView):
    queryset = FIAS_FederalSubject.objects.all()
    serializer_class = FIAS_FederalSubjectSerializer
    pagination_class = Pagination


class FIAS_LocalityView(FIAS_ObjectView):
    queryset = FIAS_Locality.objects.all()
    serializer_class = FIAS_LocalitySerializer
    pagination_class = Pagination


class FIAS_CityView(FIAS_ObjectView):
    queryset = FIAS_City.objects.all()
    serializer_class = FIAS_ObjectSerializer
    pagination_class = Pagination


class FIAS_DistrictView(FIAS_ObjectView):
    queryset = FIAS_District.objects.all()
    serializer_class = FIAS_ObjectSerializer
    pagination_class = Pagination


class FIAS_StreetView(FIAS_ObjectView):
    queryset = FIAS_Street.objects.all()
    serializer_class = FIAS_StreetSerializer
    pagination_class = Pagination
