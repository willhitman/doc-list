from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import Listing, ListingLanguages, ListingSpecialization, ListingAffiliationsAndMemberships, \
    ListingEducationalBackground, ListingExperience, AppointmentsAvailability, ListingServices
from .serializers import ListingSerializer, ListingListSerializer, ListingLanguageSerializer, \
    ListingLanguageCreateUpdateSerializer, ListingSpecializationSerializer, \
    ListingAffiliationsAndMembershipsSerializer, ListingAffiliationsAndMembershipsCreateSerializer, \
    ListingEducationalBackgroundCreateSerializers, \
    ListingEducationalBackgroundSerializers, ListingExperienceSerializer, AppointmentsAvailabilitySerializer, \
    ListingServicesSerializer, ListingServicesUpdateSerializer


class CreateListingView(CreateAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    authentication_classes = [IsAuthenticated]


class GetUpdateDeleteListingView(GenericAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    authentication_classes = [IsAuthenticated]

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
    authentication_classes = [IsAuthenticated]


class GetAllListingsByUserIdView(GenericAPIView):
    serializer_class = ListingListSerializer
    queryset = Listing.objects.all()
    authentication_classes = [IsAuthenticated]

    def get(self, request, user_id):
        listings = self.queryset.filter(user_id=user_id)
        serializer = self.serializer_class(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetListingsByListingTypeView(GenericAPIView):
    serializer_class = ListingListSerializer
    queryset = Listing.objects.all()
    authentication_classes = [IsAuthenticated]

    def get(self, request, listing_type):
        listings = self.queryset.filter(listing_type=listing_type)
        serializer = self.serializer_class(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateListingLanguageView(CreateListingView):
    serializer_class = ListingLanguageCreateUpdateSerializer
    queryset = ListingLanguages.objects.all()
    authentication_classes = [IsAuthenticated]


class GetUpdateDestroyListingLanguageView(GenericAPIView):
    serializer_class = ListingLanguageSerializer
    queryset = ListingLanguages.objects.all()
    authentication_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            listing_language = self.queryset.get(pk=pk)
        except ListingLanguages.DoesNotExist:
            return Response({'message': 'Listing Language not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing_language)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            listing_language = self.queryset.get(pk=pk)
        except ListingLanguages.DoesNotExist:
            return Response({'message': 'Listing Language not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing_language, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            listing_language = self.queryset.get(pk=pk)
        except ListingLanguages.DoesNotExist:
            return Response({'message': 'Listing Language not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            listing_language.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CreateListingSpecializationView(CreateAPIView):
    serializer_class = ListingSpecializationSerializer
    queryset = ListingSpecialization.objects.all()
    authentication_classes = [IsAuthenticated]


class GetUpdateDestroyListingSpecializationView(GenericAPIView):
    serializer_class = ListingSpecializationSerializer
    queryset = ListingSpecialization.objects.all()
    authentication_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            listing_specialization = self.queryset.get(pk=pk)
        except ListingSpecialization.DoesNotExist:
            return Response({'message': 'Listing Specialization not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing_specialization)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            listing_specialization = self.queryset.get(pk=pk)
        except ListingSpecialization.DoesNotExist:
            return Response({'message': 'Listing Specialization not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing_specialization, request.data, partial=True)
            if serializer.is_valid():
                serializer.validated_data.pop('status')
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, instance, pk):
        try:
            listing_specialization = self.queryset.get(pk=pk)
        except ListingSpecialization.DoesNotExist:
            return Response({'message': 'Listing Specialization not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            listing_specialization.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CreateListingAffiliationView(CreateAPIView):
    serializer_class = ListingAffiliationsAndMembershipsCreateSerializer
    queryset = ListingAffiliationsAndMemberships.objects.all()
    authentication_classes = [IsAuthenticated]


class GetUpdateDestroyListingAffiliationAndMembershipsView(GenericAPIView):
    serializer_class = ListingAffiliationsAndMembershipsSerializer
    queryset = ListingAffiliationsAndMemberships.objects.all()
    authentication_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            listing_affiliation = self.queryset.get(pk=pk)
        except ListingAffiliationsAndMemberships.DoesNotExist:
            return Response({'message': 'Listing Affiliations or Membership not found'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing_affiliation)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            listing_affiliation = self.queryset.get(pk=pk)
        except ListingAffiliationsAndMemberships.DoesNotExist:
            return Response({'message': 'Listing Affiliations or Membership not found'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing_affiliation, request.data, partial=True)
            if serializer.is_valid():
                serializer.validated_data.pop('status')
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            listing_affiliation = self.queryset.get(pk=pk)
        except ListingAffiliationsAndMemberships.DoesNotExist:
            return Response({'message': 'Listing Affiliations or Membership not found'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            listing_affiliation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CreateListingEducationalBackgroundView(GenericAPIView):
    serializer_class = ListingEducationalBackgroundCreateSerializers
    queryset = ListingEducationalBackground.objects.all()
    authentication_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['listing_type'] == "Practice":
                return Response({'message': 'Practice cannot have education background'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUpdateDestroyListingEducationalBackgroundView(GenericAPIView):
    serializer_class = ListingEducationalBackgroundSerializers
    queryset = ListingEducationalBackground.objects.all()
    authentication_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            listing_education = self.queryset.get(pk=pk)
        except ListingEducationalBackground.DoesNotExist:
            return Response({'message': 'Listing Education not found'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing_education)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            listing_education = self.queryset.get(pk=pk)
        except ListingEducationalBackground.DoesNotExist:
            return Response({'message': 'Listing Education not found'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing_education, request.data, partial=True)
            if serializer.is_valid():
                serializer.validated_data.pop('status')
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            listing_education = self.queryset.get(pk=pk)
        except ListingEducationalBackground.DoesNotExist:
            return Response({'message': 'Listing Education not found'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            listing_education.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CreateListingExperienceView(GenericAPIView):
    serializer_class = ListingExperienceSerializer
    queryset = ListingExperience.objects.all()
    authentication_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['listing'].listing_type == "Practice":
                return Response({'message': 'Practice cannot have Experience'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUpdateDestroyListingExperienceView(GenericAPIView):
    serializer_class = ListingExperienceSerializer
    queryset = ListingExperience.objects.all()
    authentication_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            listing_experience = self.queryset.get(pk=pk)
        except ListingExperience.DoesNotExist:
            return Response({'message': 'Listing Experience not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing_experience)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            listing_experience = self.queryset.get(pk=pk)
        except ListingExperience.DoesNotExist:
            return Response({'message': 'Listing Experience not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing_experience, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            listing_experience = self.queryset.get(pk=pk)
        except ListingExperience.DoesNotExist:
            return Response({'message': 'Listing Experience not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            listing_experience.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CreateAppointmentsAvailabilityView(CreateAPIView):
    serializer_class = AppointmentsAvailabilitySerializer
    queryset = AppointmentsAvailability.objects.all()
    authentication_classes = [IsAuthenticated]


class GetUpdateDestroyAppointmentsAvailabilityView(GenericAPIView):
    serializer_class = AppointmentsAvailabilitySerializer
    queryset = AppointmentsAvailability.objects.all()
    authentication_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            listing_appointment = self.queryset.get(pk=pk)
        except AppointmentsAvailability.DoesNotExist:
            return Response({'message': 'Listing Appointment Availability not found'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing_appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            listing_appointment = self.queryset.get(pk=pk)
        except AppointmentsAvailability.DoesNotExist:
            return Response({'message': 'Listing Appointment Availability not found'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing_appointment, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            listing_appointment = self.queryset.get(pk=pk)
        except AppointmentsAvailability.DoesNotExist:
            return Response({'message': 'Listing Appointment Availability not found'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            listing_appointment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CreateListingServicesView(CreateAPIView):
    serializer_class = ListingServicesSerializer
    queryset = ListingServices.objects.all()
    authentication_classes = [IsAuthenticated]


class GetListingServicesView(GenericAPIView):
    serializer_class = ListingServicesSerializer
    queryset = ListingServices.objects.all()
    authentication_classes = [IsAuthenticated]


    def get(self, request, pk):
        try:
            listing_service = self.queryset.get(pk=pk)
        except ListingServices.DoesNotExist:
            return Response({'message': 'Listing Service not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ListingServicesSerializer(listing_service, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateDestroyListingServicesView(GenericAPIView):
    serializer_class = ListingServicesUpdateSerializer
    queryset = ListingServices.objects.all()
    authentication_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            listing_service = self.queryset.get(pk=pk)
        except ListingServices.DoesNotExist:
            return Response({'message': 'Listing Service not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(listing_service, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            listing_service = self.queryset.get(pk=pk)
        except ListingServices.DoesNotExist:
            return Response({'message': 'Listing Service not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            listing_service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
