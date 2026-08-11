from rest_framework import serializers

from agenda.models import BloqueioAgenda, DisponibilidadeMedico


class DisponibilidadeMedicoSerializer(serializers.ModelSerializer):
    medico_nome = serializers.CharField(source="medico.nome", read_only=True)

    class Meta:
        model = DisponibilidadeMedico
        fields = (
            "id",
            "medico",
            "medico_nome",
            "dia_semana",
            "hora_inicio",
            "hora_fim",
            "duracao_consulta",
            "ativo",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        instance = DisponibilidadeMedico(**{**attrs})
        if self.instance:
            for field in ("medico", "dia_semana", "hora_inicio", "hora_fim", "duracao_consulta", "ativo"):
                setattr(instance, field, attrs.get(field, getattr(self.instance, field)))
            instance.pk = self.instance.pk
        instance.full_clean()
        return attrs


class BloqueioAgendaSerializer(serializers.ModelSerializer):
    medico_nome = serializers.CharField(source="medico.nome", read_only=True)

    class Meta:
        model = BloqueioAgenda
        fields = (
            "id",
            "medico",
            "medico_nome",
            "data",
            "hora_inicio",
            "hora_fim",
            "motivo",
            "observacao",
            "created_at",
        )
        read_only_fields = ("id", "created_at")

    def validate(self, attrs):
        instance = BloqueioAgenda(**{**attrs})
        if self.instance:
            for field in ("medico", "data", "hora_inicio", "hora_fim", "motivo", "observacao"):
                setattr(instance, field, attrs.get(field, getattr(self.instance, field)))
            instance.pk = self.instance.pk
        instance.full_clean()
        return attrs
