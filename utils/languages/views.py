from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.models import Languages
from utils.serializers import LanguagesSerializer


class CreateLanguageView(CreateAPIView):
    serializer_class = LanguagesSerializer
    queryset = Languages.objects.all()
    permission_classes = [IsAuthenticated]


class GetUpdateDestroyLanguageView(GenericAPIView):
    serializer_class = LanguagesSerializer
    queryset = Languages.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            language = self.queryset.get(pk=pk)
        except Languages.DoesNotExist:
            return Response({'message': 'Language not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(language)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            language = self.queryset.get(pk=pk)
        except Languages.DoesNotExist:
            return Response({'message': 'Language not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(language, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            language = self.queryset.get(pk=pk)
        except Languages.DoesNotExist:
            return Response({'message': 'Language not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            language.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class GetAllLanguagesView(ListAPIView):
    serializer_class = LanguagesSerializer
    queryset = Languages.objects.all()
    permission_classes = []