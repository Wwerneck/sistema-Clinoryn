from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from consultas.models import Consulta
from prontuarios.models import EvolucaoClinica, Prontuario


class EvolucaoClinicaSerializer(serializers.ModelSerializer):
    medico_nome = serializers.CharField(source="medico.nome", read_only=True)

    class Meta:
        model = EvolucaoClinica
        fields = ("id", "medico", "medico_nome", "descricao", "created_at")
        read_only_fields = fields


class ProntuarioSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source="paciente.nome_completo", read_only=True)
    medico_nome = serializers.CharField(source="medico.nome", read_only=True)
    evolucoes = EvolucaoClinicaSerializer(many=True, read_only=True)

    class Meta:
        model = Prontuario
        fields = (
            "id",
            "consulta",
            "paciente",
            "paciente_nome",
            "medico",
            "medico_nome",
            "queixa_principal",
            "sintomas",
            "historico",
            "alergias",
            "antecedentes",
            "doencas_preexistentes",
            "medicamentos_em_uso",
            "historico_familiar",
            "diagnostico",
            "observacoes",
            "evolucoes",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "consulta", "paciente", "medico", "created_at", "updated_at")


class ProntuarioWriteSerializer(serializers.ModelSerializer):
    consulta = serializers.PrimaryKeyRelatedField(queryset=Consulta.objects.none())

    class Meta:
        model = Prontuario
        fields = (
            "consulta",
            "queixa_principal",
            "sintomas",
            "historico",
            "alergias",
            "antecedentes",
            "doencas_preexistentes",
            "medicamentos_em_uso",
            "historico_familiar",
            "diagnostico",
            "observacoes",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if getattr(user, "is_authenticated", False) and getattr(user, "role", None) == "MEDICO":
            self.fields["consulta"].queryset = Consulta.objects.filter(medico=getattr(user, "medico", None))

    def create(self, validated_data):
        consulta = validated_data.pop("consulta")
        obj = Prontuario(consulta=consulta, paciente=consulta.paciente, medico=consulta.medico, **validated_data)
        try:
            obj.full_clean()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict if hasattr(exc, "message_dict") else exc.messages) from exc
        obj.save()
        from auditoria.services import log_action

        log_action(action="PRONTUARIO_ALTERADO", user=self.context["request"].user, obj=obj)
        return obj

    def update(self, instance, validated_data):
        validated_data.pop("consulta", None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        from auditoria.services import log_action

        log_action(action="PRONTUARIO_ALTERADO", user=self.context["request"].user, obj=instance)
        return instance


class EvolucaoCreateSerializer(serializers.Serializer):
    descricao = serializers.CharField()
