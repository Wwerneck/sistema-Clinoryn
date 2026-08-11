from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from consultas.models import Consulta
from consultas.services import save_appointment
from medicos.models import Medico
from pacientes.models import Paciente


class ConsultaSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source="paciente.nome_completo", read_only=True)
    medico_nome = serializers.CharField(source="medico.nome", read_only=True)
    especialidade_nome = serializers.CharField(source="especialidade.nome", read_only=True)

    class Meta:
        model = Consulta
        fields = (
            "id",
            "paciente",
            "paciente_nome",
            "medico",
            "medico_nome",
            "especialidade",
            "especialidade_nome",
            "data",
            "hora_inicio",
            "hora_fim",
            "valor",
            "status",
            "observacoes_administrativas",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "especialidade",
            "hora_fim",
            "valor",
            "status",
            "created_at",
            "updated_at",
        )


class ConsultaWriteSerializer(serializers.Serializer):
    paciente = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.none())
    medico = serializers.PrimaryKeyRelatedField(queryset=Medico.objects.none())
    data = serializers.DateField()
    hora_inicio = serializers.TimeField()
    observacoes_administrativas = serializers.CharField(required=False, allow_blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request is None:
            self.fields["paciente"].queryset = Paciente.objects.none()
            self.fields["medico"].queryset = Medico.objects.none()
            return
        user = request.user
        if not getattr(user, "is_authenticated", False):
            self.fields["paciente"].queryset = Paciente.objects.none()
            self.fields["medico"].queryset = Medico.objects.none()
            return
        patient_queryset = Paciente.objects.select_related("user")
        if user.role == "PACIENTE":
            patient_queryset = patient_queryset.filter(user=user)
        self.fields["paciente"].queryset = patient_queryset
        self.fields["medico"].queryset = Medico.objects.filter(ativo=True).select_related("especialidade")

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        return self._save(validated_data, instance=instance)

    def _save(self, validated_data, instance=None):
        if instance is not None:
            validated_data = {
                "paciente": validated_data.get("paciente", instance.paciente),
                "medico": validated_data.get("medico", instance.medico),
                "data": validated_data.get("data", instance.data),
                "hora_inicio": validated_data.get("hora_inicio", instance.hora_inicio),
                "observacoes_administrativas": validated_data.get(
                    "observacoes_administrativas",
                    instance.observacoes_administrativas,
                ),
            }
        try:
            return save_appointment(
                paciente=validated_data["paciente"],
                medico=validated_data["medico"],
                data=validated_data["data"],
                hora_inicio=validated_data["hora_inicio"],
                actor=self.context["request"].user,
                observacoes=validated_data.get("observacoes_administrativas", ""),
                instance=instance,
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError({"code": "APPOINTMENT_INVALID", "detail": exc.message}) from exc


class StatusActionSerializer(serializers.Serializer):
    detail = serializers.CharField(read_only=True)
