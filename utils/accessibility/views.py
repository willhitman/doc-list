from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response

from utils.models import Accessibility
from utils.serializers import AccessibilitySerializer
from rest_framework.permissions import IsAuthenticated

class CreateAccessibilityView(CreateAPIView):
    serializer_class = AccessibilitySerializer
    queryset = Accessibility.objects.all()
    permission_classes = [IsAuthenticated]


class GetUpdateDestroyAccessibilityView(GenericAPIView):
    serializer_class = AccessibilitySerializer
    queryset = Accessibility.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            accessibility = self.queryset.get(pk=pk)
        except Accessibility.DoesNotExist:
            return Response({'message': 'Accessibility not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(accessibility)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            accessibility = self.queryset.get(pk=pk)
        except Accessibility.DoesNotExist:
            return Response({'message': 'Accessibility not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(accessibility, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            accessibility = self.queryset.get(pk=pk)
        except Accessibility.DoesNotExist:
            return Response({'message': 'Accessibility not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            accessibility.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
