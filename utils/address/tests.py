from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from listings.models import Listing
from rest_framework.test import APIClient

from utils.models import Accessibility


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
        self.listing = Listing.objects.create(user=self.user, listing_type='Doctor')
        token_url = reverse('token-obtain-pair')
        response = self.client.post(token_url, {'username': self.user.username, 'password': '12345-th-%$'})
        self.assertEqual(response.status_code, 200)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')


    def test_address_views(self):
        request_body = {
            'door_address': '645',
            'street_one': 'Musasa',
            'street_two': 'Mutondo',
            'suburb': 'Indigenous',
            'province': 'Maaango',
            'city': 'Harare'
        }

        request_url = reverse('address')
        # Test post request
        response = self.client.post(request_url, request_body)
        self.assertEqual(response.status_code, 201)
        pk = response.data['id']
        response_dict = response.data
        response_dict.pop('id')
        self.assertDictEqual(request_body, response_dict)

        request_url = reverse('address-get-update-destroy', args=[pk])

        # Test get method
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)
        response_dict['id'] = pk
        self.assertDictEqual(response.data, response_dict)

        # Test update method
        request_body['door_address'] = '018'
        request_body['street_one'] = 'updated street'
        request_body['street_two'] = 'updated street'
        request_body['suburb'] = 'hella'
        request_body['province'] = 'Hre'
        request_body['city'] = 'Hre'

        response = self.client.put(request_url, request_body)
        self.assertEqual(response.status_code, 204)

        # Check update
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)
        response_dict = response.data
        response_dict.pop('id')
        self.assertDictEqual(response_dict, request_body)

        # Test delete method
        response = self.client.delete(request_url)
        self.assertEqual(response.status_code,204)
        # Check update
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 404)


