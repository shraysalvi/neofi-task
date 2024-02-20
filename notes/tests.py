from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User



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


class NoteViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {
            'content': 'This is a test note content'
        }
        self.invalid_payload = {
        }

    def test_create_valid_note(self):
        url = reverse('create_note')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_note(self):
        url = reverse('create_note')
        response = self.client.post(url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)