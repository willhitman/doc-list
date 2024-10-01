from django.db import IntegrityError
from rest_framework import status, serializers
from rest_framework.exceptions import ValidationError
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


class AccessibilityUpdateSerializer(ModelSerializer):
    class Meta:
        model = Accessibility
        exclude = ['date_created', 'last_updated', 'listing']


class DaysListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        print(validated_data)
        validated_days = []

        # Iterate over each item and validate
        for item in validated_data:
            if not item or 'day' not in item or not item['day']:
                raise serializers.ValidationError("Each entry must contain a valid 'day' field.")

            # Validate using the DaysSerializer
            serializer = DaysSerializer(data=item)
            if serializer.is_valid():
                validated_days.append(Days(**serializer.validated_data))
            else:
                raise serializers.ValidationError(f"Invalid data: {item}")

        # Bulk create the validated Days objects
        try:
            return Days.objects.bulk_create(validated_days)
        except IntegrityError as e:
            # Parse the IntegrityError to get the duplicate day
            if 'Duplicate entry' in str(e):
                duplicate_value = str(e).split("'")[1]  # Extract the duplicate value from the error message
                raise ValidationError(f"The day '{duplicate_value}' already exists in the database.")
            raise ValidationError("A database error occurred.")


class DaysSerializer(ModelSerializer):
    day = serializers.CharField(required=True)

    class Meta:
        model = Days
        fields = ['day']
        list_serializer_class = DaysListSerializer
