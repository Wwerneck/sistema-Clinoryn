from pathlib import Path

from django.http import FileResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

from accounts.models import User
from exames.models import Exame

from .serializers import ExameCreateSerializer, ExameSerializer


class ExameViewSet(viewsets.ModelViewSet):
    filterset_fields = ("paciente", "medico", "consulta", "tipo_exame", "data_exame")
    search_fields = ("tipo_exame", "descricao")
    ordering_fields = ("created_at", "data_exame")
    ordering = ("-created_at",)
    http_method_names = ("get", "post", "head", "options")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Exame.objects.none()
        user = self.request.user
        queryset = Exame.objects.select_related("consulta", "paciente", "medico")
        if user.role == User.Role.MEDICO:
            return queryset.filter(medico=getattr(user, "medico", None))
        if user.role == User.Role.PACIENTE:
            return queryset.filter(paciente=getattr(user, "paciente", None))
        return queryset.none()

    def get_serializer_class(self):
        if self.action == "create":
            return ExameCreateSerializer
        return ExameSerializer

    def perform_create(self, serializer):
        if self.request.user.role != User.Role.MEDICO:
            raise PermissionDenied("Somente médicos podem registrar exames.")
        serializer.save()

    def create(self, request, *args, **kwargs):
        if request.user.role != User.Role.MEDICO:
            raise PermissionDenied("Somente médicos podem registrar exames.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(ExameSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="arquivo")
    def arquivo(self, request, pk=None):
        exame = self.get_object()
        if not exame.arquivo:
            raise NotFound("Exame sem arquivo.")
        from auditoria.services import log_action

        log_action(action="EXAME_DOWNLOAD", user=request.user, obj=exame)
        return FileResponse(
            exame.arquivo.open("rb"),
            as_attachment=True,
            filename=Path(exame.arquivo.name).name,
        )
