from django.test import TestCase

from especialidades.models import Especialidade
from medicos.forms import MedicoCreateForm


class EspecialidadeCatalogTests(TestCase):
    def test_catalog_contains_all_cfm_specialties(self):
        self.assertEqual(Especialidade.objects.filter(ativo=True).count(), 55)
        self.assertTrue(
            Especialidade.objects.filter(
                nome="Patologia Clínica/Medicina Laboratorial"
            ).exists()
        )

    def test_every_cfm_specialty_has_a_description(self):
        self.assertFalse(
            Especialidade.objects.filter(ativo=True, descricao="").exists()
        )
        self.assertIn(
            "coração",
            Especialidade.objects.get(nome="Cardiologia").descricao,
        )

    def test_doctor_form_lists_only_active_specialties(self):
        inativa = Especialidade.objects.get(nome="Acupuntura")
        inativa.ativo = False
        inativa.save(update_fields=("ativo",))

        form = MedicoCreateForm()

        self.assertNotIn(inativa, form.fields["especialidade"].queryset)
        self.assertEqual(
            list(form.fields["especialidade"].queryset),
            list(
                form.fields["especialidade"].queryset.order_by("nome")
            ),
        )
