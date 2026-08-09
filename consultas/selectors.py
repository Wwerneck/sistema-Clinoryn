from .models import Consulta


def appointments_for_date(*, date):
    return Consulta.objects.filter(data=date).select_related("paciente", "medico", "especialidade").order_by("hora_inicio")
