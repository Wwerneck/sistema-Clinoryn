from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.db.models import DecimalField, Value

from .models import Pagamento


def payments_for_user(user):
    qs = Pagamento.objects.select_related(
        "consulta", "paciente", "medico", "registrado_por"
    )
    if user.role == "MEDICO":
        qs = qs.filter(medico=getattr(user, "medico", None))
    elif user.role == "PACIENTE":
        qs = qs.filter(paciente=getattr(user, "paciente", None))
    return qs


def financial_summary(qs):
    money = DecimalField(max_digits=12, decimal_places=2)
    return qs.aggregate(
        total=Count("id"),
        recebido=Coalesce(
            Sum("valor", filter=models.Q(status=Pagamento.Status.PAGO)),
            Value(0),
            output_field=money,
        ),
        pendentes=Count("id", filter=models.Q(status=Pagamento.Status.PENDENTE)),
    )
