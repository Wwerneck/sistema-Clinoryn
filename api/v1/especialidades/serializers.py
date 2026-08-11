from rest_framework import serializers

from especialidades.models import Especialidade


class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = ("id", "nome", "descricao", "ativo", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
