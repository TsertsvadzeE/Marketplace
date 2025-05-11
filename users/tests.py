from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User

class UserTests(APITestCase):

    def test_user_registration(self):
        url = reverse('user-create')
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_user_login(self):
        user = User.objects.create_user(username="mark", email="mark@example.com", password="password123", is_verified=True)
        url = reverse('token_obtain_pair')
        data = {
            "username": "mark",
            "password": "password123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
