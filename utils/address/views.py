from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from utils.models import Address
from utils.serializers import AddressSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class AddressCreateView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressReadUpdateDestroyView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get(self, request, pk):
        address = Address.objects.get(pk=pk)
        serializer = self.serializer_class(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        address = Address.objects.get(pk=pk)
        serializer = self.serializer_class(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = Address.objects.get(pk=pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

