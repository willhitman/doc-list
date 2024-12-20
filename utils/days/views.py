from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.models import Days
from utils.serializers import DaysSerializer


class CreateDayView(ListCreateAPIView):
    serializer_class = DaysSerializer
    queryset = Days.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.all()

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


class GetUpdateDestroyView(GenericAPIView):
    serializer_class = DaysSerializer
    queryset = Days.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        days = get_object_or_404(Days, pk=pk)
        serializer = self.serializer_class(days)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        day = get_object_or_404(Days, pk=pk)
        serializer = self.serializer_class(Days,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        day = get_object_or_404(Days, pk=pk)
        day.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)