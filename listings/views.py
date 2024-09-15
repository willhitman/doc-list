from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .files import handle_images, handle_pdfs
from .models import Listing, ListingLanguages, ListingSpecialization, ListingAffiliationsAndMemberships, \
    ListingEducationalBackground, ListingExperience, AppointmentsAvailability, ListingServices
from .serializers import ListingSerializer, ListingListSerializer, ListingLanguageSerializer, \
    ListingLanguageCreateUpdateSerializer, ListingSpecializationSerializer, \
    ListingAffiliationsAndMembershipsSerializer, ListingAffiliationsAndMembershipsCreateSerializer, \
    ListingEducationalBackgroundCreateSerializers, \
    ListingEducationalBackgroundSerializers, ListingExperienceSerializer, AppointmentsAvailabilitySerializer, \
    ListingServicesSerializer, ListingServicesUpdateSerializer, ListingProfilePictureSerializer, \
    ListingSpecializationFileSerializer, ListingAffiliationsAndMembershipsFileSerializer


class CreateListingView(CreateAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    permission_classes = [IsAuthenticated]


class GetUpdateDeleteListingView(GenericAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    permission_classes = [IsAuthenticated]

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


class ProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        listing = get_object_or_404(Listing, pk=pk)
        serializer = ListingProfilePictureSerializer(listing)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        listing = get_object_or_404(Listing, pk=pk, user=request.user)

        if 'profile-picture' not in request.FILES:
            return Response({'message': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            uploaded_file = request.FILES['profile-picture']
            listing.profile_picture = handle_images(uploaded_file)
            listing.save()
        return Response({'message': 'Image saved successfully'}, status=status.HTTP_200_OK)


class GetAllListingsView(ListAPIView):
    serializer_class = ListingListSerializer
    queryset = Listing.objects.all()
    permission_classes = [IsAuthenticated]


class GetAllListingsByUserIdView(GenericAPIView):
    serializer_class = ListingListSerializer
    queryset = Listing.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        listings = self.queryset.filter(user_id=user_id)
        serializer = self.serializer_class(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetListingsByListingTypeView(GenericAPIView):
    serializer_class = ListingListSerializer
    queryset = Listing.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, listing_type):
        listings = self.queryset.filter(listing_type=listing_type)
        serializer = self.serializer_class(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateListingLanguageView(CreateListingView):
    serializer_class = ListingLanguageCreateUpdateSerializer
    queryset = ListingLanguages.objects.all()
    permission_classes = [IsAuthenticated]


class GetUpdateDestroyListingLanguageView(GenericAPIView):
    serializer_class = ListingLanguageSerializer
    queryset = ListingLanguages.objects.all()
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]


class GetUpdateDestroyListingSpecializationView(GenericAPIView):
    serializer_class = ListingSpecializationSerializer
    queryset = ListingSpecialization.objects.all()
    permission_classes = [IsAuthenticated]

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


class SpecializationFileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        specialization = get_object_or_404(ListingSpecialization, pk=pk)
        serializer = ListingSpecializationFileSerializer(specialization)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        specialization = get_object_or_404(ListingSpecialization, pk=pk, listing__user=request.user)

        if 'file' not in request.FILES:
            return Response({'message': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            uploaded_file = request.FILES['file']
            specialization.file = handle_pdfs(uploaded_file)
            specialization.save()
        return Response({'message': 'File saved successfully'}, status=status.HTTP_200_OK)


class CreateListingAffiliationView(CreateAPIView):
    serializer_class = ListingAffiliationsAndMembershipsCreateSerializer
    queryset = ListingAffiliationsAndMemberships.objects.all()
    permission_classes = [IsAuthenticated]


class GetUpdateDestroyListingAffiliationAndMembershipsView(GenericAPIView):
    serializer_class = ListingAffiliationsAndMembershipsSerializer
    queryset = ListingAffiliationsAndMemberships.objects.all()
    permission_classes = [IsAuthenticated]

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


class AffiliationAndMembershipsFileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        affiliation = get_object_or_404(ListingSpecialization, pk=pk)
        serializer = ListingAffiliationsAndMembershipsFileSerializer(affiliation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        affiliation = get_object_or_404(ListingSpecialization, pk=pk, listing__user=request.user)

        if 'file' not in request.FILES:
            return Response({'message': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            uploaded_file = request.FILES['file']
            affiliation.file = handle_pdfs(uploaded_file)
            affiliation.save()
        return Response({'message': 'File saved successfully'}, status=status.HTTP_200_OK)


class CreateListingEducationalBackgroundView(GenericAPIView):
    serializer_class = ListingEducationalBackgroundCreateSerializers
    queryset = ListingEducationalBackground.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['listing'].listing_type == "Practice":
                return Response({'message': 'Practice cannot have education background'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUpdateDestroyListingEducationalBackgroundView(GenericAPIView):
    serializer_class = ListingEducationalBackgroundSerializers
    queryset = ListingEducationalBackground.objects.all()
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]


class GetUpdateDestroyAppointmentsAvailabilityView(GenericAPIView):
    serializer_class = AppointmentsAvailabilitySerializer
    queryset = AppointmentsAvailability.objects.all()
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]


class GetUpdateDestroyListingServicesView(GenericAPIView):
    serializer_class = ListingServicesUpdateSerializer
    queryset = ListingServices.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            listing_service = self.queryset.get(pk=pk)
        except ListingServices.DoesNotExist:
            return Response({'message': 'Listing Service not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ListingServicesSerializer(listing_service, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

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


class GetListingServicesByListingIdView(GenericAPIView):
    serializer_class = ListingServicesUpdateSerializer
    queryset = ListingServices.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, listing_id):
        listing_services = self.queryset.filter(listing_id=listing_id)
        serializer = self.serializer_class(listing_services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
