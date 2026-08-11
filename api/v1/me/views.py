from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveAPIView

from accounts.models import User
from api.v1.auth.serializers import UserMeSerializer
from api.v1.consultas.serializers import ConsultaSerializer
from api.v1.exames.serializers import ExameSerializer
from api.v1.financeiro.serializers import PagamentoSerializer
from api.v1.prescricoes.serializers import PrescricaoSerializer
from consultas.models import Consulta
from exames.models import Exame
from financeiro.models import Pagamento
from prescricoes.models import Prescricao


class MeProfileView(RetrieveAPIView):
    serializer_class = UserMeSerializer

    def get_object(self):
        return self.request.user


class PatientMeMixin:
    def get_patient(self):
        if self.request.user.role != User.Role.PACIENTE:
            raise PermissionDenied("Endpoint disponível apenas para pacientes.")
        return getattr(self.request.user, "paciente", None)


class MeConsultasView(PatientMeMixin, ListAPIView):
    serializer_class = ConsultaSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Consulta.objects.none()
        patient = self.get_patient()
        return patient.consultas.select_related("paciente", "medico", "especialidade").order_by("data", "hora_inicio")


class MeExamesView(PatientMeMixin, ListAPIView):
    serializer_class = ExameSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Exame.objects.none()
        patient = self.get_patient()
        return patient.exames.select_related("consulta", "paciente", "medico").order_by("-created_at")


class MePrescricoesView(PatientMeMixin, ListAPIView):
    serializer_class = PrescricaoSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Prescricao.objects.none()
        patient = self.get_patient()
        return patient.prescricoes.select_related("consulta", "paciente", "medico").prefetch_related("itens").order_by("-created_at")


class MePagamentosView(PatientMeMixin, ListAPIView):
    serializer_class = PagamentoSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Pagamento.objects.none()
        patient = self.get_patient()
        return patient.pagamentos.select_related("consulta", "paciente", "medico").order_by("-created_at")
