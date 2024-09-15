from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.models import Services
from utils.serializers import ServicesSerializer


class CreateServiceView(CreateAPIView):
    serializer_class = ServicesSerializer
    queryset = Services.objects.all()
    permission_classes = [IsAuthenticated]


class GetUpdateDestroyServicesView(GenericAPIView):
    serializer_class = ServicesSerializer
    queryset = Services.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            service = self.queryset.get(pk=pk)
        except Services.DoesNotExist:
            return Response({'message': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(service)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            service = self.queryset.get(pk=pk)
        except Services.DoesNotExist:
            return Response({'message': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(service, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            service = self.queryset.get(pk=pk)
        except Services.DoesNotExist:
            return Response({'message': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class GetAllServicesView(ListAPIView):
    serializer_class = ServicesSerializer
    queryset = Services.objects.all()
    permission_classes = []
