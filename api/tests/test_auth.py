from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


class ApiAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="api_admin",
            password="StrongPass123!",
            email="admin@example.com",
            role="ADMIN",
        )

    def test_login_returns_access_and_refresh_tokens(self):
        response = self.client.post(
            reverse("api-v1:auth:login"),
            {"username": "api_admin", "password": "StrongPass123!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_me_requires_authentication(self):
        response = self.client.get(reverse("api-v1:auth:me"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_current_user_without_sensitive_fields(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse("api-v1:auth:me"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "api_admin")
        self.assertEqual(response.data["role"], "ADMIN")
        self.assertNotIn("password", response.data)
        self.assertNotIn("is_staff", response.data)
        self.assertNotIn("is_superuser", response.data)
