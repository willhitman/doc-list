from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response

from .models import Listing
from .serializers import ListingSerializer, ListingListSerializer


class CreateListingView(CreateAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    authentication_classes = []


class GetUpdateDeleteListingView(GenericAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    authentication_classes = []

    def get(self, listing_id):
        listings = self.queryset.get(pk=listing_id)
        serializer = self.serializer_class(listings)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, listing_id):
        try:
            listing = self.queryset.get(pk=listing_id)
        except listing.DoesNotExist:
            return Response({'message': 'Listing does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, listing_id):
        try:
            listing = self.queryset.get(pk=listing_id)
        except listing.DoesNotExist:
            return Response({'message': 'Listing does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            listing.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class GetAllListingsView(ListAPIView):
    serializer_class = ListingListSerializer
    queryset = Listing.objects.all()
    authentication_classes = []


class GetAllListingsByUserIdView(GenericAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    authentication_classes = []

    def get(self, user_id):
        listings = self.queryset.filter(user_id=user_id)
        serializer = self.serializer_class(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetListingsByListingTypeView(GenericAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    authentication_classes = []

    def get(self, listing):
        listings = self.queryset.filter(listing=listing)
        serializer = self.serializer_class(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
