from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer, ModelSerializer

from utils.models import Address, Insurance, Languages, Services, Accessibility, Days


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        exclude = ['date_created', 'last_updated']


class InsuranceSerializer(ModelSerializer):
    class Meta:
        model = Insurance
        exclude = ['date_created', 'last_updated']


class LanguagesSerializer(ModelSerializer):
    class Meta:
        model = Languages
        exclude = ['date_created', 'last_updated']


class ServicesSerializer(ModelSerializer):
    class Meta:
        model = Services
        exclude = ['date_created', 'last_updated']


class AccessibilitySerializer(ModelSerializer):
    class Meta:
        model = Accessibility
        exclude = ['date_created', 'last_updated']


class DaysSerializer(ModelSerializer):
    class Meta:
        model = Days
        exclude = ['date_created', 'last_updated']
