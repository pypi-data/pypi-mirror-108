from django.contrib import admin

from smpl_fias.models import *


class FIAS_BaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'aoid', 'live_status')
    search_fields = ('name', 'aoid', 'aoguid',)
    list_filter = ('level', 'live_status')


@admin.register(FIAS_Object)
class FIAS_ObjectAdmin(FIAS_BaseAdmin):
    pass


@admin.register(FIAS_FederalSubject)
class FIAS_FederalSubjectAdmin(FIAS_BaseAdmin):
    pass


@admin.register(FIAS_Locality)
class FIAS_LocalityAdmin(FIAS_BaseAdmin):
    pass


@admin.register(FIAS_Street)
class FIAS_StreetAdmin(FIAS_BaseAdmin):
    pass
