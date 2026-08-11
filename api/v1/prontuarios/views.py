from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from accounts.models import User
from prontuarios.models import EvolucaoClinica, Prontuario

from .serializers import EvolucaoCreateSerializer, ProntuarioSerializer, ProntuarioWriteSerializer


class ProntuarioViewSet(viewsets.ModelViewSet):
    filterset_fields = ("paciente", "medico", "consulta")
    ordering_fields = ("created_at", "updated_at", "consulta__data")
    ordering = ("-consulta__data", "-consulta__hora_inicio")
    http_method_names = ("get", "post", "patch", "head", "options")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Prontuario.objects.none()
        user = self.request.user
        queryset = Prontuario.objects.select_related("consulta", "paciente", "medico").prefetch_related("evolucoes")
        if user.role == User.Role.MEDICO:
            return queryset.filter(medico=getattr(user, "medico", None))
        return queryset.none()

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return ProntuarioWriteSerializer
        return ProntuarioSerializer

    def perform_create(self, serializer):
        if self.request.user.role != User.Role.MEDICO:
            raise PermissionDenied("Somente médicos podem registrar prontuários.")
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user.role != User.Role.MEDICO:
            raise PermissionDenied("Somente médicos podem alterar prontuários.")
        serializer.save()

    def create(self, request, *args, **kwargs):
        if request.user.role != User.Role.MEDICO:
            raise PermissionDenied("Somente médicos podem registrar prontuários.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(ProntuarioSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(ProntuarioSerializer(serializer.instance).data)

    @action(detail=True, methods=["post"], url_path="evolucoes")
    def evolucoes(self, request, pk=None):
        prontuario = self.get_object()
        serializer = EvolucaoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        EvolucaoClinica.objects.create(
            prontuario=prontuario,
            medico=getattr(request.user, "medico", None),
            descricao=serializer.validated_data["descricao"],
        )
        from auditoria.services import log_action

        log_action(action="EVOLUCAO_CLINICA_CRIADA", user=request.user, obj=prontuario)
        return Response(ProntuarioSerializer(prontuario).data, status=status.HTTP_201_CREATED)
