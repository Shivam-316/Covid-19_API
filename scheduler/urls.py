from django.urls import path
from .views import runTests

urlpatterns=[
    path('', runTests, name='test')
]