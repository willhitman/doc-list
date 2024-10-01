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

    def test_accessibility_views(self):
        request_url = reverse('accessibility')

        request_data = {
            'listing': self.listing.id,
            'parking': False,
            'wheel_chair_accessible_parking': False,
            'wifi': True,
            'infotainment': False,
            'additional_notes': False,
        }
        # post with correct data
        request = self.client.post(request_url, request_data)
        self.assertEqual(request.status_code, 201)
        database_data = Accessibility.objects.get(listing_id=1)
        self.assertEquals(database_data.listing_id, request.data['listing'])

        # Try to duplicate
        request = self.client.post(request_url, request_data)
        self.assertEqual(request.status_code, 400)

        # Test post with missing listing
        del request_data['listing']
        request = self.client.post(request_url, request_data)
        self.assertEqual(request.status_code, 400)

        # test with wrong listing id
        request_data['listing'] = 0
        request = self.client.post(request_url, request_data)
        self.assertEqual(request.status_code, 400)

        # Test get method with wrong id
        request_url = reverse('accessibility-get-update-destroy', args=[0])
        request = self.client.get(request_url)
        self.assertEqual(request.status_code, 404)

        # Test no authorization
        request_url = reverse('accessibility-get-update-destroy', args=[1])
        request = self.unauthenticated_client.get(request_url)
        self.assertEqual(request.status_code, 401)

        # Test get method authorization
        request = self.client.get(request_url)
        self.assertEqual(request.status_code, 200)

        # Test update method authorization
        del request_data['listing']
        request_data['parking'] = True
        request_data['wheel_chair_accessible_parking'] = True
        request_data['wifi'] = True
        request_data['infotainment'] = True
        request_data['additional_notes'] = True

        request = self.client.put(request_url, request_data)
        self.assertEqual(request.status_code, 204)

        # Test delete request
        request = self.client.delete(request_url)
        self.assertEqual(request.status_code, 204)













