from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.models import Days
from utils.serializers import DaysSerializer


class CreateDayView(CreateAPIView):
    serializer_class = DaysSerializer
    queryset = Days.objects.all()
    permission_classes = [IsAuthenticated]