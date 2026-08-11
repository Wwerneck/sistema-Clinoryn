from django.db.models import Q
from rest_framework import viewsets

from accounts.models import User
from pacientes.models import Paciente

from .serializers import (
    PacienteCreateSerializer,
    PacienteDetailSerializer,
    PacienteListSerializer,
)


class PacienteViewSet(viewsets.ModelViewSet):
    filterset_fields = ("cpf", "email", "estado", "cidade")
    search_fields = ("nome_completo", "cpf", "telefone", "email")
    ordering_fields = ("nome_completo", "created_at", "updated_at")
    ordering = ("nome_completo",)
    http_method_names = ("get", "post", "patch", "head", "options")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Paciente.objects.none()
        user = self.request.user
        queryset = Paciente.objects.select_related("user")
        if user.role == User.Role.PACIENTE:
            return queryset.filter(user=user)
        if user.role == User.Role.MEDICO:
            medico = getattr(user, "medico", None)
            return queryset.filter(consultas__medico=medico).distinct()
        if user.role in (User.Role.ADMIN, User.Role.RECEPCAO):
            query = self.request.query_params.get("nome", "").strip()
            if query:
                queryset = queryset.filter(Q(nome_completo__icontains=query))
            return queryset
        return queryset.none()

    def get_serializer_class(self):
        if self.action == "create":
            return PacienteCreateSerializer
        if self.action == "list":
            return PacienteListSerializer
        return PacienteDetailSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action == "create":
            from api.permissions import IsAdminOrReceptionRole

            return [IsAdminOrReceptionRole()]
        return permissions
