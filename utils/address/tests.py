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
