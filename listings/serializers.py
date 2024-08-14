from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserSerializer
from listings.models import Listing
from utils.serializers import AddressSerializer


class ListingSerializer(ModelSerializer):
    class Meta:
        model = Listing
        exclude = ['date_created', 'last_updated']


class ListingListSerializer(ModelSerializer):
    address = AddressSerializer()
    user = UserSerializer()

    class Meta:
        model = Listing
        exclude = ['date_created', 'last_updated']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.listing == "Practice":
            representation.pop('user',None)
        return representation
