from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from django.http import Http404
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.db.models import Sum, Count, Q
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from datetime import date
from .models import StatewiseData
from .serializers import StateVaccineSerializer, RegionWiseCasesSerializer, RegionWiseVaccinationSerializer, RegionWiseVaccineTypeSerializer

## Login API
#@csrf_exempt
#@api_view(['POST'])
#def LoginView(request):
#    username = request.data.get("username")
#    password = request.data.get("password")
#    if username is None or password is None:
#        return Response(
#            {'error':"Please Provide valid information for `username` and `password`"},
#            status=HTTP_400_BAD_REQUEST
#        )
#    user = authenticate(username = username,password = password)
#    if not user:
#        return Response(
#            {'error': 'Invalid Credentials'},
#            status=HTTP_404_NOT_FOUND
#        )
#    token,_ = Token.objects.get_or_create(user = user)
#    return Response(
#        {'token': token.key},
#        status=HTTP_200_OK
#    )

# Generic API

class RegionAdd(generics.CreateAPIView):
    """
    This can be used to add records to database.

    """
    queryset = StatewiseData.objects.all()
    serializer_class = StateVaccineSerializer
    permission_classes = (IsAdminUser,)

class RegionsCodes(APIView):
    """
    Retuns distinct state names along with their code/key.
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        context = StatewiseData.objects.values('state','key').distinct()
        return Response(context)



# Covid Cases API 

class RegionsCases(APIView):
    """
    Returns total and today confirmed cases for each state.
    """
    renderer_classes = [JSONRenderer]
    
    def get(self, request, format=None):
        context = StatewiseData.objects.values('state').annotate(total_cases = Sum('confirmed'), today_cases = Sum('confirmed', filter = Q(date = date.today())))
        return Response(context)


class RegionCases(APIView):
    """
    Returns confirmed, recovered and deceased cases for a region aggregated over past month.
    """
    renderer_classes = [JSONRenderer]

    def get_object(self, region):
        try:
            return StatewiseData.objects.filter(key=region).aggregate(Sum('confirmed'),Sum('recovered'),Sum('deceased'))
        except ObjectDoesNotExist:
            raise Http404
    
    def get(self, request, region, format=None):
        context = self.get_object(region)
        return Response(context)

class RegionCasesTimeSeries(APIView):
    """
    Returns confirmed, recovered and deceased cases for a region as a timeseries over past month.
    """
    def get(self, request, region, format=None):
        cases = StatewiseData.objects.filter(key=region)
        serializer = RegionWiseCasesSerializer(cases,many=True)
        return Response(serializer.data)


# Vaccination API
class RegionVaccinationTimeSeries(APIView):
    """
    Returns first and second dose timeseries of vaccinations in a region over past month.
    """
    def get(self, request, region, format=None):
        cases = StatewiseData.objects.filter(key=region)
        serializer = RegionWiseVaccinationSerializer(cases,many=True)
        return Response(serializer.data)

class AgeVaccinationTimeSeries(APIView):
    """
    Retuns count of individuals vaccinated over past month age wise binned into 18-45, 45-60 and 60+.
    """
    renderer_classes = [JSONRenderer]
    
    def get(self, request,region, format=None):
        context = StatewiseData.objects.filter(key=region).values_list('age18_45','age45_60','age60').aggregate(Sum('age18_45'),Sum('age45_60'),Sum('age60'))
        return Response(context)

class GenderVaccinationTotal(APIView):
    """
    Retuns count of individuals vaccinated over past month gender wise binned.
    """
    renderer_classes = [JSONRenderer]
    
    def get(self, request,region, format=None):
        context = StatewiseData.objects.filter(key=region).aggregate(Sum('male_vcc'),Sum('female_vcc'),Sum('transgender_vcc'))
        return Response(context)

class TypeVaccinationTimeSeries(APIView):
    """
     Retuns count of vaccinations adminstered over past month grouped into categories.
    """
    def get(self, request, region, format=None):
        cases = StatewiseData.objects.filter(key=region)
        serializer = RegionWiseVaccineTypeSerializer(cases,many=True)
        return Response(serializer.data)