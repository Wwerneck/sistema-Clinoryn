from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from accounts.models import User
from financeiro.models import Pagamento
from financeiro.selectors import financial_summary, payments_for_user

from .serializers import FinancialSummarySerializer, PagamentoSerializer, PagamentoWriteSerializer


class PagamentoViewSet(viewsets.ModelViewSet):
    filterset_fields = ("consulta", "paciente", "medico", "status", "forma_pagamento")
    ordering_fields = ("created_at", "data_pagamento", "valor", "status")
    ordering = ("-created_at",)
    http_method_names = ("get", "post", "patch", "head", "options")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Pagamento.objects.none()
        return payments_for_user(self.request.user)

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return PagamentoWriteSerializer
        return PagamentoSerializer

    def _ensure_write_permission(self):
        if self.request.user.role not in (User.Role.ADMIN, User.Role.RECEPCAO):
            raise PermissionDenied("Perfil sem permissão para registrar pagamentos.")

    def create(self, request, *args, **kwargs):
        self._ensure_write_permission()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pagamento = serializer.save()
        return Response(PagamentoSerializer(pagamento).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        self._ensure_write_permission()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        pagamento = serializer.save()
        return Response(PagamentoSerializer(pagamento).data)

    @action(detail=False, methods=["get"])
    def resumo(self, request):
        serializer = FinancialSummarySerializer(financial_summary(self.get_queryset()))
        return Response(serializer.data)
