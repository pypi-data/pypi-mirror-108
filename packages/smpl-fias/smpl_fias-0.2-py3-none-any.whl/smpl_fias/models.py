
from django.db import models

from .managers import *

__all__ = [
    'FIAS_Object',
    'FIAS_FederalSubject',
    'FIAS_City',
    'FIAS_District',
    'FIAS_Locality',
    'FIAS_Street',
]


class FIAS_Object(models.Model):

    aoid = models.CharField(max_length=36, unique=True, primary_key=True, verbose_name='Идентификатор')
    parent_guid = models.CharField(max_length=36, null=True, blank=True, db_index=True,
                                   verbose_name='Идентификатор объекта родительского объекта')
    aoguid = models.CharField(max_length=36, db_index=True, verbose_name='Идентификатор')
    level = models.PositiveIntegerField(default=0, verbose_name='Уровень адресного объекта')
    name = models.CharField(max_length=120, verbose_name='Название')
    short_name = models.CharField(max_length=500, verbose_name='Короткое название')
    region_code = models.CharField(max_length=2, null=True, blank=True, verbose_name='Код региона')
    area_code = models.CharField(max_length=3, null=True, blank=True, verbose_name='Код района')
    city_code = models.CharField(max_length=3, null=True, blank=True, verbose_name='Код города')
    postal_code = models.CharField(max_length=6, null=True, blank=True, verbose_name='Почтовый индекс')
    okato = models.CharField(max_length=11, null=True, blank=True, verbose_name='OKATO')
    oktmo = models.CharField(max_length=11, null=True, blank=True, verbose_name='OKTMO')
    kladr = models.CharField(max_length=17, null=True, blank=True, verbose_name='КЛАДР')
    cent_status = models.PositiveIntegerField(null=True, blank=True, verbose_name='Статус центра')
    live_status = models.BooleanField(default=True, verbose_name='Активность')

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты ФИАС'

    def __str__(self):
        if self.short_name in ['р-н', 'край']:
            return f'{self.name} {self.short_name}'

        return f'{self.short_name} {self.name}'

    @property
    def label(self):
        if self.level == 1:
            return self.name
        elif self.short_name in ['р-н']:
            return f'{self.name} {self.short_name}'
        else:
            return f'{self.short_name} {self.name}'


class FIAS_FederalSubject(FIAS_Object):

    class Meta:
        verbose_name = 'Субъект'
        verbose_name_plural = 'Субъекты Российской Федерации'
        default_permissions = ()
        proxy = True

    objects = FIAS_FederalSubjectManager()


class FIAS_Locality(FIAS_Object):

    class Meta:
        verbose_name = 'Населенный пункт'
        verbose_name_plural = 'Населенные пункты'
        default_permissions = ()
        proxy = True

    objects = FIAS_LocalityManager()


class FIAS_City(FIAS_Object):

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        default_permissions = ()
        proxy = True

    objects = FIAS_CityManager()


class FIAS_District(FIAS_Object):

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'
        default_permissions = ()
        proxy = True

    objects = FIAS_DistrictManager()


class FIAS_Street(FIAS_Object):

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'
        default_permissions = ()
        proxy = True

    objects = FIAS_StreetManager()
