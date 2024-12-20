from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from rest_framework.test import APIClient


class AccessibilityTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Define class level resources here

    def setUp(self):
        self.client = APIClient()
        self.unauthenticated_client = APIClient()
        # Setup which runs before every individual test
        self.user = User.objects.create_user(username='test@gmail.com', password='12345-th-%$')
        token_url = reverse('token-obtain-pair')
        response = self.client.post(token_url, {'username': self.user.username, 'password': '12345-th-%$'})
        self.assertEqual(response.status_code, 200)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_accessibility_views(self):
        request_object = {
            'day': 'Monday'
        }

        # Test single object creation
        request_url = reverse('create-day')
        response = self.client.post(request_url, request_object)
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, {'day': 'Monday'})

        # Test List Object creation

        request_list_object = [
            {'day': 'Tuesday'},
            {'day': 'Wednesday'}
        ]

        response = self.client.post(request_url, request_list_object, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, request_list_object)

        # Test with missing empty dictionary
        response = self.client.post(request_url, {})
        self.assertEqual(response.status_code, 400)

        # Test with missing empty list
        response = self.client.post(request_url, [], format='json')
        self.assertEqual(response.status_code, 201)  # Empty list will return 201 which is a bug

        request_list_object = [
            request_object,
            {'day': 'Tuesday'},
            {'day': 'Wednesday'}
        ]
        # Test get list
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.data, request_list_object)
