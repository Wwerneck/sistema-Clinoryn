from rest_framework import serializers

from pacientes.models import Paciente


class PacienteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = (
            "id",
            "nome_completo",
            "cpf",
            "telefone",
            "email",
            "cidade",
            "estado",
        )
        read_only_fields = fields


class PacienteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = (
            "id",
            "nome_completo",
            "cpf",
            "data_nascimento",
            "sexo",
            "telefone",
            "email",
            "endereco",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "estado",
            "cep",
            "contato_emergencia",
            "telefone_emergencia",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "cpf", "created_at", "updated_at")


class PacienteCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Paciente
        fields = (
            "username",
            "password",
            "nome_completo",
            "cpf",
            "data_nascimento",
            "sexo",
            "telefone",
            "email",
            "endereco",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "estado",
            "cep",
            "contato_emergencia",
            "telefone_emergencia",
        )

    def create(self, validated_data):
        from accounts.models import User
        from accounts.services import create_user_with_profile

        user = create_user_with_profile(
            role=User.Role.PACIENTE,
            profile_model=Paciente,
            profile_data=validated_data,
        )
        return user.paciente
