from django.urls import path
from .views import collectData
urlpatterns = [
    path('',collectData, name='data_collector')
]