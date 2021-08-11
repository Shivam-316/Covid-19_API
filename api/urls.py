from django.urls import path
from .views import (
    #LoginView,
    RegionAdd, RegionCases, RegionCasesTimeSeries, RegionsCases, RegionsCodes,
    RegionVaccinationTimeSeries, AgeVaccinationTimeSeries, GenderVaccinationTotal, TypeVaccinationTimeSeries, RegionsVaccination
)
urlpatterns=[
    #path('api/v1/login',LoginView),

    path('add', RegionAdd.as_view(),name='addRecords'),
    path('regions/info',RegionsCodes.as_view()),

    path('regions/cases/todaytotal', RegionsCases.as_view()),
    path('region/<str:region>/cases/timeseries', RegionCasesTimeSeries.as_view()),
    path('region/<str:region>/cases/', RegionCases.as_view()),

    path('regions/vaccine/todaytotal', RegionsVaccination.as_view()),
    path('region/<str:region>/vaccine/timeseries', RegionVaccinationTimeSeries.as_view()),
    path('region/<str:region>/vaccine/agewise', AgeVaccinationTimeSeries.as_view()),
    path('region/<str:region>/vaccine/genderwise', GenderVaccinationTotal.as_view()),
    path('region/<str:region>/vaccine/typewise', TypeVaccinationTimeSeries.as_view())
]
