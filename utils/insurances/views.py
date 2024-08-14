from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from utils.models import Insurance
from utils.serializers import InsuranceSerializer


class InsuranceCreateView(GenericAPIView):
    permission_classes = []
    serializer_class = InsuranceSerializer
    queryset = Insurance.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsuranceGetAll(GenericAPIView):
    permission_classes = []
    serializer_class = InsuranceSerializer
    queryset = Insurance.objects.all()

    def get(self, request):
        insurances = self.queryset.all()
        serializer = self.serializer_class(insurances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

