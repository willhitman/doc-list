from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from rest_framework.test import APIClient


class InsuranceTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.client = APIClient()
        self.unauthenticated_client = APIClient()
        self.user = User.objects.create_user(username='test@gmail.com', password='12345-th-%$')
        token_url = reverse('token-obtain-pair')
        response = self.client.post(token_url, {'username': self.user.username, 'password': '12345-th-%$'})
        self.assertEqual(response.status_code, 200)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_insurance_views(self):
        request_body = {
            'name': 'SHONA-'
        }
        request_url = reverse('insurance')

        # Test single item
        response = self.client.post(request_url, request_body)
        pk = response.data['id']
        self.assertEqual(response.status_code, 201)

        # Test bulk create
        request_bulk_body = [
            {'name': 'ENGLISH'},
            {'name': 'FRENCH'}
        ]
        response = self.client.post(request_url, request_bulk_body, format='json')
        self.assertEqual(response.status_code, 201)

        request_url = reverse('insurance-get-update-destroy', args=[pk])

        # Test get by id
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

        # Test update
        update_body = {
            'name': 'SHONA'
        }
        response = self.client.put(request_url, update_body)
        self.assertEqual(response.status_code, 204)

        # Test delete
        response = self.client.delete(request_url)
        self.assertEqual(response.status_code, 204)

        # Try to get deleted object
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 404)

        # Test get all
        request_url = reverse('get-all-insurance')
        response = self.unauthenticated_client.get(request_url)
        self.assertEqual(response.status_code, 200)
