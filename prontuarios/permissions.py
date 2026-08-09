from consultas.models import Consulta


def doctor_has_patient_link(*, medico, paciente):
    return Consulta.objects.filter(medico=medico, paciente=paciente).exists()
