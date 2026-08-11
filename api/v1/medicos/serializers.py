from rest_framework import serializers

from consultas.models import Consulta
from medicos.models import Medico


class MedicoSerializer(serializers.ModelSerializer):
    especialidade_nome = serializers.CharField(source="especialidade.nome", read_only=True)

    class Meta:
        model = Medico
        fields = (
            "id",
            "nome",
            "crm",
            "especialidade",
            "especialidade_nome",
            "telefone",
            "email",
            "valor_consulta",
            "duracao_consulta",
            "ativo",
        )
        read_only_fields = fields


class MedicoConsultaSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source="paciente.nome_completo", read_only=True)
    especialidade_nome = serializers.CharField(source="especialidade.nome", read_only=True)

    class Meta:
        model = Consulta
        fields = (
            "id",
            "paciente",
            "paciente_nome",
            "especialidade",
            "especialidade_nome",
            "data",
            "hora_inicio",
            "hora_fim",
            "status",
        )
        read_only_fields = fields
