from rest_framework import serializers

from consultas.models import Consulta
from financeiro.models import Pagamento


class PagamentoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source="paciente.nome_completo", read_only=True)
    medico_nome = serializers.CharField(source="medico.nome", read_only=True)

    class Meta:
        model = Pagamento
        fields = (
            "id",
            "consulta",
            "paciente",
            "paciente_nome",
            "medico",
            "medico_nome",
            "valor",
            "forma_pagamento",
            "status",
            "data_pagamento",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class PagamentoWriteSerializer(serializers.Serializer):
    consulta = serializers.PrimaryKeyRelatedField(queryset=Consulta.objects.all())
    forma_pagamento = serializers.ChoiceField(choices=Pagamento.Forma.choices)
    status = serializers.ChoiceField(choices=Pagamento.Status.choices)

    def create(self, validated_data):
        from financeiro.services import save_payment

        return save_payment(
            consulta=validated_data["consulta"],
            forma_pagamento=validated_data["forma_pagamento"],
            status=validated_data["status"],
            actor=self.context["request"].user,
        )

    def update(self, instance, validated_data):
        from financeiro.services import save_payment

        consulta = validated_data.get("consulta", instance.consulta)
        return save_payment(
            consulta=consulta,
            forma_pagamento=validated_data.get("forma_pagamento", instance.forma_pagamento),
            status=validated_data.get("status", instance.status),
            actor=self.context["request"].user,
        )


class FinancialSummarySerializer(serializers.Serializer):
    total = serializers.IntegerField()
    recebido = serializers.DecimalField(max_digits=12, decimal_places=2)
    pendentes = serializers.IntegerField()
