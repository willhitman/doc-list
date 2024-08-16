from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response

from .models import Listing, ListingLanguages
from .serializers import ListingSerializer, ListingListSerializer, ListingLanguageSerializer


class CreateListingView(CreateAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    authentication_classes = []


class GetUpdateDeleteListingView(GenericAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    authentication_classes = []

    def get(self, request, pk):
        try:
            listing = self.queryset.get(pk=pk)
        except Listing.DoesNotExist:
            return Response({'message': 'Listing does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            listing = self.queryset.get(pk=pk)
        except Listing.DoesNotExist:
            return Response({'message': 'Listing does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            listing = self.queryset.get(pk=pk)
        except Listing.DoesNotExist:
            return Response({'message': 'Listing does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            listing.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class GetAllListingsView(ListAPIView):
    serializer_class = ListingListSerializer
    queryset = Listing.objects.all()
    authentication_classes = []


class GetAllListingsByUserIdView(GenericAPIView):
    serializer_class = ListingListSerializer
    queryset = Listing.objects.all()
    authentication_classes = []

    def get(self, request, user_id):
        listings = self.queryset.filter(user_id=user_id)
        serializer = self.serializer_class(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetListingsByListingTypeView(GenericAPIView):
    serializer_class = ListingListSerializer
    queryset = Listing.objects.all()
    authentication_classes = []

    def get(self, request, listing_type):
        listings = self.queryset.filter(listing_type=listing_type)
        serializer = self.serializer_class(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateListingLanguageView(CreateListingView):
    serializer_class = ListingLanguageSerializer
    queryset = ListingLanguages.objects.all()
    authentication_classes = []


class GetUpdateDestroyView(GenericAPIView):
    serializer_class = ListingLanguageSerializer
    queryset = ListingLanguages.objects.all()
    authentication_classes = []

    def get(self, request, pk):
        pass
