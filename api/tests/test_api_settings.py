from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import User


class ApiProductionSettingsTests(TestCase):
    @override_settings(
        CORS_ALLOWED_ORIGINS=["https://app.clinoryn.example"],
        CORS_ALLOW_CREDENTIALS=False,
    )
    def test_cors_allows_configured_origin_only(self):
        allowed = self.client.options(
            reverse("api-v1:auth:me"),
            HTTP_ORIGIN="https://app.clinoryn.example",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        denied = self.client.options(
            reverse("api-v1:auth:me"),
            HTTP_ORIGIN="https://evil.example",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )

        self.assertEqual(
            allowed.headers["access-control-allow-origin"],
            "https://app.clinoryn.example",
        )
        self.assertNotIn("access-control-allow-origin", denied.headers)

    @override_settings(API_DOCS_REQUIRE_AUTH=True)
    def test_api_schema_can_require_authentication(self):
        anonymous = self.client.get(reverse("api-schema"))
        user = User.objects.create_user(
            username="docs-user",
            password="test",
            role=User.Role.ADMIN,
        )
        self.client.force_login(user)
        authenticated = self.client.get(reverse("api-schema"))

        self.assertEqual(anonymous.status_code, 401)
        self.assertEqual(authenticated.status_code, 200)
