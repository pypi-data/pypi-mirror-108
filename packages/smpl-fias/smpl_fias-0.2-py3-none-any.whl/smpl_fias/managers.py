
from django.db import models

__all__ = [
    'FIAS_FederalSubjectManager',
    'FIAS_LocalityManager',
    'FIAS_StreetManager',
    'FIAS_CityManager',
    'FIAS_DistrictManager'
]


class FIAS_FederalSubjectManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(level=1)


class FIAS_LocalityManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(level__in=[6])


class FIAS_StreetManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(level=7)


class FIAS_CityManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(level=4).exclude(city_code='000')


class FIAS_DistrictManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(level=3).exclude(area_code='000')
