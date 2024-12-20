from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.response import Response

from utils.models import Insurance
from utils.serializers import InsuranceSerializer
from rest_framework.permissions import IsAuthenticated


class CreateInsuranceView(ListCreateAPIView):
    serializer_class = InsuranceSerializer
    queryset = Insurance.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            many = True
        else:
            many = False

        serializer = self.get_serializer(data=request.data, many=many)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUpdateDestroyInsuranceView(GenericAPIView):
    serializer_class = InsuranceSerializer
    queryset = Insurance.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            insurance = self.queryset.get(pk=pk)
        except Insurance.DoesNotExist:
            return Response({'message': 'Insurance not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(insurance)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            insurance = self.queryset.get(pk=pk)
        except Insurance.DoesNotExist:
            return Response({'message': 'Insurance not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(insurance, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            insurance = self.queryset.get(pk=pk)
        except Insurance.DoesNotExist:
            return Response({'message': 'Insurance not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            insurance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class GetAllInsurancesView(ListAPIView):
    serializer_class = InsuranceSerializer
    queryset = Insurance.objects.all()
    permission_classes = []
