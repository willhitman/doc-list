from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserSerializer
from listings.models import Listing, ListingLanguages, ListingSpecialization, ListingAffiliationsAndMemberships, \
    ListingEducationalBackground, ListingExperience, AppointmentsAvailability, Days, ListingServices
from utils.models import Address, Languages, Services
from utils.serializers import AddressSerializer, LanguagesSerializer, ServicesSerializer


# function to handle creation or update of listing languages
def handle_languages(listing, languages_data):
    existing_languages = set(listing.languages.all())
    new_languages = []

    for lang in languages_data:
        language_instance, created = ListingLanguages.objects.get_or_create(**lang)
        if language_instance not in existing_languages:
            new_languages.append(language_instance)

    if new_languages:
        listing.languages.add(*new_languages)
        listing.save()

    ListingLanguages.objects.filter(listings=None).delete()


class ListingLanguageSerializer(ModelSerializer):
    class Meta:
        model = ListingLanguages
        exclude = ['date_created', 'last_updated']


class ListingLanguageCreateUpdateSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField(min_value=1, required=True)
    languages = ListingLanguageSerializer(many=True, required=True)

    def create(self, validated_data):
        listing_id = validated_data.pop('listing_id')
        languages_data = validated_data.pop('languages', [])

        try:
            listing = Listing.objects.get(pk=listing_id)
        except Listing.DoesNotExist:
            raise serializers.ValidationError({"listing_id": "Listing not found."})

        with transaction.atomic():
            handle_languages(listing=listing, languages_data=languages_data)
        return listing

    def update(self, instance, validated_data):
        languages_data = validated_data.pop('languages', [])

        with transaction.atomic():
            handle_languages(listing=instance, languages_data=languages_data)

        return instance


class ListingSerializer(ModelSerializer):
    address = AddressSerializer()
    languages = ListingLanguageSerializer(many=True)

    class Meta:
        model = Listing
        exclude = ['date_created', 'last_updated']

    def create(self, validated_data):
        address_data = validated_data.pop("address", None)
        languages = validated_data.pop("languages", [])
        with transaction.atomic():
            if address_data:
                address = Address.objects.create(**address_data)
                validated_data['address'] = address
            listing = Listing.objects.create(**validated_data)
            if languages:
                handle_languages(listing=listing, languages_data=languages)

        return listing

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", None)
        languages_data = validated_data.pop("languages", [])
        with transaction.atomic():
            if address_data:
                address, created = Address.objects.update_or_create(
                    id=instance.address.pk,
                    defaults=address_data
                )
                instance.address = address

                for attr, value in validated_data.items():
                    setattr(instance, attr, value)

                instance.save()

                if languages_data:
                    handle_languages(listing=instance, languages_data=languages_data)

                ListingLanguages.objects.filter(listings=None).delete()

        return instance


class ListingListSerializer(ModelSerializer):
    address = AddressSerializer()
    user = UserSerializer()
    languages = ListingLanguageSerializer(many=True)

    class Meta:
        model = Listing
        exclude = ['date_created', 'last_updated']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.listing_type == "Practice":
            representation.pop('user', None)
        return representation


class ListingSpecializationSerializer(ModelSerializer):
    class Meta:
        model = ListingSpecialization
        exclude = ['date_created', 'last_updated', 'file']


class ListingAffiliationsAndMembershipsCreateSerializer(ModelSerializer):
    class Meta:
        model = ListingAffiliationsAndMemberships
        exclude = ['date_created', 'last_updated', 'status']


class ListingAffiliationsAndMembershipsSerializer(ModelSerializer):
    class Meta:
        model = ListingAffiliationsAndMemberships
        exclude = ['date_created', 'last_updated']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.status == 'active' and instance.expiry_date < timezone.now().date():
            representation['status'] = 'expired'
            instance.status = 'expired'
            instance.save()
        return representation


class ListingEducationalBackgroundCreateSerializers(ModelSerializer):
    class Meta:
        model = ListingEducationalBackground
        exclude = ['date_created', 'last_updated', 'status']


class ListingEducationalBackgroundSerializers(ModelSerializer):
    class Meta:
        model = ListingEducationalBackground
        exclude = ['date_created', 'last_updated']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.status == 'pending' and instance.end_date > timezone.now().date():
            representation['status'] = 'finished'
            instance.status = 'finished'
            instance.save()
        return representation


class ListingExperienceSerializer(ModelSerializer):
    class Meta:
        model = ListingExperience
        exclude = ['date_created', 'last_updated', 'still_employed']


class DaysCreateSerializer(ModelSerializer):
    class Meta:
        model = Days
        exclude = ['date_created', 'last_updated']


class AppointmentsAvailabilitySerializer(ModelSerializer):
    days = DaysCreateSerializer(required=True, many=True)

    class Meta:
        model = AppointmentsAvailability
        exclude = ['date_created', 'last_updated']

    def create(self, validated_data):
        days_data = validated_data.pop('days')
        days = [Days.objects.create(**day) for day in days_data]

        appointment = AppointmentsAvailability.objects.create(**validated_data)

        appointment.days.set(days)

        appointment.save()

        return appointment

    def update(self, instance, validated_data):
        days_data = validated_data.pop('days', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        instance.days.set(days_data)

        return instance


class ListingServicesSerializer(ModelSerializer):

    class Meta:
        model = ListingServices
        exclude = ['date_created', 'last_updated']

    def create(self, validated_data):
        service_data = validated_data.pop('service', [])
        with transaction.atomic():
            _services = [Services.objects.create(**serv) for serv in service_data]

            listing_service = ListingServices.objects.create(**validated_data)
            listing_service.service.set(_services)
            listing_service.save()
            return listing_service

    def update(self, instance, validated_data):
        service_data = validated_data.pop('service', [])
        existing_services = set(instance.service.all())
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            new_services = []

            for service in service_data:
                service_instance, created = ListingServices.objects.get_or_create(**service)
                if service_instance not in existing_services:
                    new_services.append(service_instance)

            if new_services:
                instance.service.add(*new_services)

            ListingServices.objects.filter(listing=None).delete()


class ListingServicesUpdateSerializer(ModelSerializer):
    class Meta:
        model = ListingServices
        exclude = ['date_created', 'last_updated']
