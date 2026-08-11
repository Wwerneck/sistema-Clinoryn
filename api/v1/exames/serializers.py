from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from consultas.models import Consulta
from exames.models import Exame


class ExameSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source="paciente.nome_completo", read_only=True)
    medico_nome = serializers.CharField(source="medico.nome", read_only=True)
    possui_arquivo = serializers.SerializerMethodField()

    class Meta:
        model = Exame
        fields = (
            "id",
            "consulta",
            "paciente",
            "paciente_nome",
            "medico",
            "medico_nome",
            "tipo_exame",
            "descricao",
            "data_exame",
            "possui_arquivo",
            "observacoes",
            "created_at",
        )
        read_only_fields = fields

    @extend_schema_field(serializers.BooleanField)
    def get_possui_arquivo(self, obj):
        return bool(obj.arquivo)


class ExameCreateSerializer(serializers.ModelSerializer):
    consulta = serializers.PrimaryKeyRelatedField(queryset=Consulta.objects.none())

    class Meta:
        model = Exame
        fields = ("consulta", "tipo_exame", "descricao", "data_exame", "arquivo", "observacoes")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if getattr(user, "is_authenticated", False) and getattr(user, "role", None) == "MEDICO":
            self.fields["consulta"].queryset = Consulta.objects.filter(medico=getattr(user, "medico", None))

    def create(self, validated_data):
        consulta = validated_data.pop("consulta")
        exame = Exame.objects.create(
            consulta=consulta,
            paciente=consulta.paciente,
            medico=consulta.medico,
            **validated_data,
        )
        from auditoria.services import log_action

        log_action(
            action="EXAME_REGISTRADO",
            user=self.context["request"].user,
            obj=exame,
            metadata={"possui_arquivo": bool(exame.arquivo)},
        )
        return exame
