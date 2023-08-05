
from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('fias/federal_subject', views.FIAS_FederalSubjectView)
router.register('fias/locality', views.FIAS_LocalityView)
router.register('fias/street', views.FIAS_StreetView)
router.register('fias/city', views.FIAS_CityView)
router.register('fias/district', views.FIAS_DistrictView)

urlpatterns = [
    path('', include(router.urls)),
]
