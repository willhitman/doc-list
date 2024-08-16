import json

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.core import serializers
from .models import User
from accounts.serializers import UserCreateSerializer


class CreateAccountView(GenericAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        user_data = {
            'first_name': None if request.data.get('first_name') == '' else request.data.get('first_name'),
            'last_name': None if request.data.get('last_name') == '' else request.data.get('last_name'),
            'username': None if request.data.get('email') == '' else request.data.get('email'),
            'gender': None if request.data.get('gender') == '' else request.data.get('gender'),
            'email': None if request.data.get('email') == '' else request.data.get('email'),
        }

        password = None if request.data.get('password') == '' else request.data.get('password')

        serializer = self.serializer_class(data=user_data, partial=True)
        if serializer.is_valid():
            user = User.objects.create(**serializer.data)
            user.username = serializer.validated_data['email']
            user.set_password(password)
            user.save()
            return Response({'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CheckServicesView(GenericAPIView):
#     serializer_class = UserServiceAccountsSerializer
#     queryset = User.objects.all()
#     authentication_classes = []
#
#     def get(self, request, user_id):
#         try:
#             user = self.queryset.get(pk=user_id)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             record = UserServiceAccounts.objects.filter(user_id=user.pk)
#             service_accounts = get_user_service_accounts(record)
#             print(service_accounts)
#             return Response(data=service_accounts, status=status.HTTP_200_OK)
