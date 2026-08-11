from rest_framework import viewsets

from accounts.models import User
from api.permissions import IsAdminRole
from especialidades.models import Especialidade

from .serializers import EspecialidadeSerializer


class EspecialidadeViewSet(viewsets.ModelViewSet):
    serializer_class = EspecialidadeSerializer
    filterset_fields = ("ativo",)
    search_fields = ("nome", "descricao")
    ordering_fields = ("nome", "created_at")
    ordering = ("nome",)
    http_method_names = ("get", "post", "patch", "head", "options")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Especialidade.objects.none()
        queryset = Especialidade.objects.all()
        if self.request.user.role == User.Role.ADMIN:
            return queryset
        return queryset.filter(ativo=True)

    def get_permissions(self):
        if self.action in ("create", "partial_update"):
            return [IsAdminRole()]
        return super().get_permissions()
