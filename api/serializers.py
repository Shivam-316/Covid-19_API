from rest_framework import serializers
from .models import StatewiseData

class RegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatewiseData
        fields = '__all__'

class RegionWiseCasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatewiseData
        fields = ['state','date','confirmed','recovered','deceased']

class RegionWiseVaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatewiseData
        fields = ['state','date','first_dose','second_dose']

class RegionWiseVaccineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatewiseData
        fields = ['state','date','total_covishield','total_covaxin','total_sputnik']