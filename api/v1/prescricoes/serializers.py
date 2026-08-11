from django.db import transaction
from rest_framework import serializers

from consultas.models import Consulta
from prescricoes.models import ItemPrescricao, Prescricao


class ItemPrescricaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPrescricao
        fields = ("id", "medicamento", "dosagem", "frequencia", "duracao", "orientacoes")
        read_only_fields = ("id",)


class PrescricaoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source="paciente.nome_completo", read_only=True)
    medico_nome = serializers.CharField(source="medico.nome", read_only=True)
    itens = ItemPrescricaoSerializer(many=True, read_only=True)

    class Meta:
        model = Prescricao
        fields = (
            "id",
            "consulta",
            "paciente",
            "paciente_nome",
            "medico",
            "medico_nome",
            "observacoes",
            "itens",
            "created_at",
        )
        read_only_fields = fields


class PrescricaoCreateSerializer(serializers.Serializer):
    consulta = serializers.PrimaryKeyRelatedField(queryset=Consulta.objects.none())
    observacoes = serializers.CharField(required=False, allow_blank=True)
    itens = ItemPrescricaoSerializer(many=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if getattr(user, "is_authenticated", False) and getattr(user, "role", None) == "MEDICO":
            self.fields["consulta"].queryset = Consulta.objects.filter(medico=getattr(user, "medico", None))

    def validate_itens(self, value):
        if not value:
            raise serializers.ValidationError("Informe ao menos um item.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        itens = validated_data.pop("itens")
        consulta = validated_data.pop("consulta")
        prescricao = Prescricao.objects.create(
            consulta=consulta,
            paciente=consulta.paciente,
            medico=consulta.medico,
            observacoes=validated_data.get("observacoes", ""),
        )
        ItemPrescricao.objects.bulk_create(
            [ItemPrescricao(prescricao=prescricao, **item) for item in itens]
        )
        from auditoria.services import log_action

        log_action(
            action="PRESCRICAO_CRIADA",
            user=self.context["request"].user,
            obj=prescricao,
            metadata={"itens": len(itens)},
        )
        return prescricao
