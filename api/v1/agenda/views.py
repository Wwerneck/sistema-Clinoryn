from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from accounts.models import User
from agenda.models import BloqueioAgenda, DisponibilidadeMedico

from .serializers import BloqueioAgendaSerializer, DisponibilidadeMedicoSerializer


class DoctorOwnedAgendaMixin:
    def get_queryset_for_role(self, queryset):
        user = self.request.user
        if user.role == User.Role.MEDICO:
            return queryset.filter(medico=getattr(user, "medico", None))
        if user.role in (User.Role.ADMIN, User.Role.RECEPCAO):
            return queryset
        return queryset.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == User.Role.RECEPCAO:
            raise PermissionDenied("Recepção possui acesso somente de leitura à agenda.")
        if user.role == User.Role.MEDICO:
            medico = getattr(user, "medico", None)
            if serializer.validated_data["medico"] != medico:
                raise PermissionDenied("Médico só pode alterar a própria agenda.")
        elif user.role != User.Role.ADMIN:
            raise PermissionDenied("Perfil sem permissão para alterar agenda.")
        serializer.save()

    def perform_update(self, serializer):
        self.perform_create(serializer)

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role == User.Role.RECEPCAO:
            raise PermissionDenied("Recepção possui acesso somente de leitura à agenda.")
        if user.role == User.Role.MEDICO and instance.medico != getattr(user, "medico", None):
            raise PermissionDenied("Médico só pode alterar a própria agenda.")
        if user.role not in (User.Role.ADMIN, User.Role.MEDICO):
            raise PermissionDenied("Perfil sem permissão para alterar agenda.")
        instance.delete()


class DisponibilidadeMedicoViewSet(DoctorOwnedAgendaMixin, viewsets.ModelViewSet):
    serializer_class = DisponibilidadeMedicoSerializer
    filterset_fields = ("medico", "dia_semana", "ativo")
    ordering_fields = ("dia_semana", "hora_inicio", "created_at")
    ordering = ("medico__nome", "dia_semana", "hora_inicio")
    http_method_names = ("get", "post", "patch", "delete", "head", "options")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return DisponibilidadeMedico.objects.none()
        queryset = DisponibilidadeMedico.objects.select_related("medico", "medico__especialidade")
        return self.get_queryset_for_role(queryset)


class BloqueioAgendaViewSet(DoctorOwnedAgendaMixin, viewsets.ModelViewSet):
    serializer_class = BloqueioAgendaSerializer
    filterset_fields = ("medico", "data", "motivo")
    ordering_fields = ("data", "hora_inicio", "created_at")
    ordering = ("-data", "hora_inicio")
    http_method_names = ("get", "post", "patch", "delete", "head", "options")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return BloqueioAgenda.objects.none()
        queryset = BloqueioAgenda.objects.select_related("medico", "medico__especialidade")
        return self.get_queryset_for_role(queryset)
