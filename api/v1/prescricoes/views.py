from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from accounts.models import User
from prescricoes.models import Prescricao

from .serializers import PrescricaoCreateSerializer, PrescricaoSerializer


class PrescricaoViewSet(viewsets.ModelViewSet):
    filterset_fields = ("paciente", "medico", "consulta")
    ordering_fields = ("created_at",)
    ordering = ("-created_at",)
    http_method_names = ("get", "post", "head", "options")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Prescricao.objects.none()
        user = self.request.user
        queryset = Prescricao.objects.select_related("consulta", "paciente", "medico").prefetch_related("itens")
        if user.role == User.Role.MEDICO:
            return queryset.filter(medico=getattr(user, "medico", None))
        if user.role == User.Role.PACIENTE:
            return queryset.filter(paciente=getattr(user, "paciente", None))
        return queryset.none()

    def get_serializer_class(self):
        if self.action == "create":
            return PrescricaoCreateSerializer
        return PrescricaoSerializer

    def perform_create(self, serializer):
        if self.request.user.role != User.Role.MEDICO:
            raise PermissionDenied("Somente médicos podem criar prescrições.")
        serializer.save()

    def create(self, request, *args, **kwargs):
        if request.user.role != User.Role.MEDICO:
            raise PermissionDenied("Somente médicos podem criar prescrições.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(PrescricaoSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
