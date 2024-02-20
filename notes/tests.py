from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class UserSignupTest(APITestCase):

    def test_user_signup_success(self):
        """
        Test user signup with valid data.
        """
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Test@password1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_signup_failure(self):
        """
        Test user signup with invalid data.
        """
        url = reverse('signup')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
