from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserSerializer
from listings.models import Listing, ListingLanguages
from utils.models import Address, Languages
from utils.serializers import AddressSerializer, LanguagesSerializer


class ListingSerializer(ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Listing
        exclude = ['date_created', 'last_updated']

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        languages = validated_data.pop("languages")

        if address_data:
            address = Address.objects.create(**address_data)
            validated_data['address'] = address
        listing = Listing.objects.create(**validated_data)
        if languages:
            languages = [Languages.objects.filter(pk_in=languages)]
            listing.languages.set(languages)
        return listing

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", None)
        languages_data = validated_data.pop("languages", [])

        if address_data:
            address, created = Address.objects.update_or_create(
                id=instance.address.pk,
                defaults=address_data
            )
            instance.address = address

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

            if languages_data is not None:
                instance.languages.set(languages_data)

        return instance


class ListingListSerializer(ModelSerializer):
    address = AddressSerializer()
    user = UserSerializer()
    languages = LanguagesSerializer()

    class Meta:
        model = Listing
        exclude = ['date_created', 'last_updated']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.listing_type == "Practice":
            representation.pop('user', None)
        return representation


class ListingLanguageSerializer(ModelSerializer):
    class Meta:
        model = ListingLanguages
        exclude = ['date_created', 'last_updated']
