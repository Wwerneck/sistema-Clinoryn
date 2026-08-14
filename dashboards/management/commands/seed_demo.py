from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounts.models import User
from especialidades.models import Especialidade
from medicos.models import Medico
from pacientes.models import Paciente
from recepcao.models import Recepcionista


class Command(BaseCommand):
    help = "Cria dados demonstrativos idempotentes em um ambiente DEMO_MODE."

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEMO_MODE:
            raise CommandError("Defina DEMO_MODE=True antes de criar dados demonstrativos.")

        specialty, _ = Especialidade.objects.get_or_create(
            nome="Clínica Geral", defaults={"descricao": "Atendimento clínico geral"}
        )
        admin = self._user(
            "demo_admin", User.Role.ADMIN, is_staff=True, is_superuser=True
        )
        doctor_user = self._user("demo_medico", User.Role.MEDICO)
        reception_user = self._user("demo_recepcao", User.Role.RECEPCAO)
        patient_user = self._user("demo_paciente", User.Role.PACIENTE)
        Medico.objects.get_or_create(
            user=doctor_user,
            defaults={
                "nome": "Dra. Marina Demo",
                "crm": "DEMO-CRM-001",
                "especialidade": specialty,
                "telefone": "11999990001",
                "email": "medico@demo.local",
                "valor_consulta": 250,
                "duracao_consulta": 30,
            },
        )
        Recepcionista.objects.get_or_create(
            user=reception_user,
            defaults={
                "nome": "Rafaela Demo",
                "telefone": "11999990002",
                "cargo": Recepcionista.Cargo.RECEPCIONISTA,
            },
        )
        Paciente.objects.get_or_create(
            user=patient_user,
            defaults={
                "nome_completo": "Paulo Paciente Demo",
                "cpf": "52998224725",
                "data_nascimento": "1990-01-01",
                "sexo": Paciente.Sexo.NAO_INFORMADO,
                "telefone": "11999990003",
                "email": "paciente@demo.local",
                "endereco": "Rua Demonstração",
                "numero": "100",
                "bairro": "Centro",
                "cidade": "São Paulo",
                "estado": "SP",
                "cep": "01001000",
            },
        )
        self.stdout.write(
            self.style.SUCCESS(
                "Dados demonstrativos criados/atualizados. Senha: Demo@123456"
            )
        )
        self.stdout.write(f"Administrador: {admin.username}")

    def _user(self, username, role, **flags):
        user, _ = User.objects.get_or_create(
            username=username, defaults={"role": role, **flags}
        )
        user.role = role
        for name, value in flags.items():
            setattr(user, name, value)
        user.set_password("Demo@123456")
        user.save()
        return user
