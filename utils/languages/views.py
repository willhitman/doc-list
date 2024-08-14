from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response

from utils.models import Languages
from utils.serializers import LanguagesSerializer


class CreateLanguagesView(CreateAPIView):
    serializer_class = LanguagesSerializer
    queryset = Languages.objects.all()
    authentication_classes = []


class ListLanguages(ListAPIView):
    serializer_class = LanguagesSerializer
    queryset = Languages.objects.all()
    authentication_classes = []

class LanguageGetUpdateDestroyView(GenericAPIView):
    pass