from datetime import datetime, timedelta

from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from accounts.models import User
from agenda.models import BloqueioAgenda, DisponibilidadeMedico
from consultas.models import Consulta
from consultas.services import ACTIVE, cancel_appointment, transition_status

from .serializers import ConsultaSerializer, ConsultaWriteSerializer


class ConsultaViewSet(viewsets.ModelViewSet):
    filterset_fields = ("paciente", "medico", "especialidade", "data", "status")
    search_fields = ("paciente__nome_completo", "medico__nome")
    ordering_fields = ("data", "hora_inicio", "created_at", "status")
    ordering = ("data", "hora_inicio")
    http_method_names = ("get", "post", "patch", "head", "options")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Consulta.objects.none()
        user = self.request.user
        queryset = Consulta.objects.select_related("paciente", "medico", "especialidade")
        if user.role == User.Role.PACIENTE:
            return queryset.filter(paciente=getattr(user, "paciente", None))
        if user.role == User.Role.MEDICO:
            return queryset.filter(medico=getattr(user, "medico", None))
        if user.role in (User.Role.ADMIN, User.Role.RECEPCAO):
            return queryset
        return queryset.none()

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return ConsultaWriteSerializer
        return ConsultaSerializer

    def perform_create(self, serializer):
        if self.request.user.role not in (User.Role.ADMIN, User.Role.RECEPCAO, User.Role.PACIENTE):
            raise PermissionDenied("Perfil sem permissão para agendar consulta.")
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user.role not in (User.Role.ADMIN, User.Role.RECEPCAO, User.Role.PACIENTE):
            raise PermissionDenied("Perfil sem permissão para reagendar consulta.")
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        output = ConsultaSerializer(serializer.instance, context=self.get_serializer_context())
        return Response(output.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        output = ConsultaSerializer(serializer.instance, context=self.get_serializer_context())
        return Response(output.data)

    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        appointment = self.get_object()
        if request.user.role not in (User.Role.ADMIN, User.Role.RECEPCAO, User.Role.PACIENTE):
            raise PermissionDenied("Perfil sem permissão para cancelar consulta.")
        try:
            appointment = cancel_appointment(appointment=appointment, actor=request.user)
        except DjangoValidationError as exc:
            return Response({"code": "APPOINTMENT_CANCEL_INVALID", "detail": exc.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ConsultaSerializer(appointment).data)

    @action(detail=True, methods=["post"], url_path="confirmar")
    def confirmar(self, request, pk=None):
        return self._transition(Consulta.Status.CONFIRMADA)

    @action(detail=True, methods=["post"], url_path="check-in")
    def check_in(self, request, pk=None):
        return self._transition(Consulta.Status.PACIENTE_CHEGOU)

    @action(detail=True, methods=["post"], url_path="aguardar")
    def aguardar(self, request, pk=None):
        return self._transition(Consulta.Status.AGUARDANDO)

    @action(detail=True, methods=["post"], url_path="iniciar")
    def iniciar(self, request, pk=None):
        return self._transition(Consulta.Status.EM_ATENDIMENTO)

    @action(detail=True, methods=["post"], url_path="finalizar")
    def finalizar(self, request, pk=None):
        return self._transition(Consulta.Status.CONCLUIDA)

    @action(detail=True, methods=["post"], url_path="nao-compareceu")
    def nao_compareceu(self, request, pk=None):
        return self._transition(Consulta.Status.NAO_COMPARECEU)

    def _transition(self, new_status):
        appointment = self.get_object()
        self._check_status_permission(new_status)
        try:
            appointment = transition_status(appointment=appointment, new_status=new_status, actor=self.request.user)
        except DjangoValidationError as exc:
            return Response({"code": "APPOINTMENT_STATUS_INVALID", "detail": exc.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ConsultaSerializer(appointment).data)

    def _check_status_permission(self, new_status):
        role = self.request.user.role
        reception_statuses = {
            Consulta.Status.CONFIRMADA,
            Consulta.Status.PACIENTE_CHEGOU,
            Consulta.Status.AGUARDANDO,
            Consulta.Status.NAO_COMPARECEU,
        }
        doctor_statuses = {Consulta.Status.EM_ATENDIMENTO, Consulta.Status.CONCLUIDA}
        if role == User.Role.ADMIN:
            return
        if role == User.Role.RECEPCAO and new_status in reception_statuses:
            return
        if role == User.Role.MEDICO and new_status in doctor_statuses:
            return
        raise PermissionDenied("Perfil sem permissão para aplicar este status.")

    @action(detail=False, methods=["get"], url_path="horarios-disponiveis")
    def horarios_disponiveis(self, request):
        medico_id = request.query_params.get("medico")
        data_raw = request.query_params.get("data")
        if not medico_id or not data_raw:
            return Response({"detail": "Informe medico e data."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = datetime.strptime(data_raw, "%Y-%m-%d").date()
        except ValueError:
            return Response({"detail": "Data inválida. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        slots = available_slots(medico_id=medico_id, data=data)
        return Response({"results": slots})


def available_slots(*, medico_id, data):
    from medicos.models import Medico

    try:
        medico = Medico.objects.get(pk=medico_id, ativo=True)
    except Medico.DoesNotExist:
        return []
    slots = []
    for availability in DisponibilidadeMedico.objects.filter(medico=medico, dia_semana=data.weekday(), ativo=True):
        start = timezone.make_aware(datetime.combine(data, availability.hora_inicio))
        end_limit = timezone.make_aware(datetime.combine(data, availability.hora_fim))
        duration = timedelta(minutes=medico.duracao_consulta)
        while start + duration <= end_limit:
            end = start + duration
            if start > timezone.now() and not _slot_blocked(medico=medico, data=data, start=start.time(), end=end.time()):
                slots.append({"hora_inicio": start.time(), "hora_fim": end.time()})
            start = end
    return slots


def _slot_blocked(*, medico, data, start, end):
    if BloqueioAgenda.objects.filter(medico=medico, data=data, hora_inicio__lt=end, hora_fim__gt=start).exists():
        return True
    return Consulta.objects.filter(
        medico=medico,
        data=data,
        status__in=ACTIVE,
        hora_inicio__lt=end,
        hora_fim__gt=start,
    ).exists()
