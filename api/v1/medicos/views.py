from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from accounts.models import User
from agenda.models import DisponibilidadeMedico
from medicos.models import Medico

from .serializers import MedicoConsultaSerializer, MedicoSerializer


class MedicoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MedicoSerializer
    filterset_fields = ("especialidade", "ativo", "crm")
    search_fields = ("nome", "crm", "especialidade__nome")
    ordering_fields = ("nome", "created_at")
    ordering = ("nome",)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Medico.objects.none()
        queryset = Medico.objects.select_related("especialidade", "user")
        if self.request.user.role == User.Role.ADMIN:
            return queryset
        return queryset.filter(ativo=True)

    @action(detail=True, methods=["get"])
    def consultas(self, request, pk=None):
        medico = self.get_object()
        if request.user.role == User.Role.MEDICO and getattr(request.user, "medico", None) != medico:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Médico sem acesso a esta agenda.")
        queryset = medico.consultas.select_related("paciente", "especialidade").order_by("data", "hora_inicio")
        page = self.paginate_queryset(queryset)
        serializer = MedicoConsultaSerializer(page or queryset, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def agenda(self, request, pk=None):
        medico = self.get_object()
        disponibilidades = DisponibilidadeMedico.objects.filter(medico=medico, ativo=True).order_by("dia_semana", "hora_inicio")
        data = [
            {
                "id": item.id,
                "dia_semana": item.dia_semana,
                "hora_inicio": item.hora_inicio,
                "hora_fim": item.hora_fim,
                "duracao_consulta": item.duracao_consulta,
            }
            for item in disponibilidades
        ]
        return Response(data)
