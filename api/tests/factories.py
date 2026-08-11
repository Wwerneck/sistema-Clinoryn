from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model

from especialidades.models import Especialidade
from medicos.models import Medico
from pacientes.models import Paciente


def create_user(*, username, role):
    return get_user_model().objects.create_user(
        username=username,
        password="StrongPass123!",
        email=f"{username}@example.com",
        role=role,
    )


def create_paciente(*, username="paciente", nome="Paciente Teste", cpf="39053344705"):
    user = create_user(username=username, role="PACIENTE")
    return Paciente.objects.create(
        user=user,
        nome_completo=nome,
        cpf=cpf,
        data_nascimento=date(1990, 1, 1),
        sexo=Paciente.Sexo.NAO_INFORMADO,
        telefone="11999999999",
        email=f"{username}@example.com",
        endereco="Rua A",
        numero="10",
        bairro="Centro",
        cidade="São Paulo",
        estado="SP",
        cep="01001000",
    )


def create_medico(*, username="medico", nome="Medico Teste", crm="CRM123"):
    user = create_user(username=username, role="MEDICO")
    especialidade, _ = Especialidade.objects.get_or_create(nome="Clínica médica")
    return Medico.objects.create(
        user=user,
        nome=nome,
        crm=crm,
        especialidade=especialidade,
        telefone="1133333333",
        email=f"{username}@example.com",
        valor_consulta=Decimal("200.00"),
        duracao_consulta=30,
    )
