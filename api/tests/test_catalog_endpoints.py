from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from api.tests.factories import create_paciente, create_user
from especialidades.models import Especialidade


class EspecialidadeApiTests(APITestCase):
    def setUp(self):
        self.admin = create_user(username="admin", role=User.Role.ADMIN)
        self.patient = create_paciente()

    def test_authenticated_user_can_list_active_specialties(self):
        Especialidade.objects.create(nome="Teste API Ativa", ativo=True)
        Especialidade.objects.create(nome="Teste API Inativa", ativo=False)
        self.client.force_authenticate(self.patient.user)

        response = self.client.get(reverse("api-v1:especialidade-list"), {"search": "Teste API"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [item["nome"] for item in response.data["results"]]
        self.assertIn("Teste API Ativa", names)
        self.assertNotIn("Teste API Inativa", names)

    def test_only_admin_can_create_specialty(self):
        self.client.force_authenticate(self.patient.user)
        denied = self.client.post(reverse("api-v1:especialidade-list"), {"nome": "Neuro"}, format="json")

        self.client.force_authenticate(self.admin)
        allowed = self.client.post(reverse("api-v1:especialidade-list"), {"nome": "Neuro"}, format="json")

        self.assertEqual(denied.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(allowed.status_code, status.HTTP_201_CREATED)
