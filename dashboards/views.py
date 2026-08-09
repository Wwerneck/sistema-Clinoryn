from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from accounts.models import User
from accounts.permissions import roles_required
from pacientes.models import Paciente
from .selectors import admin_dashboard_data, patient_dashboard_data


@login_required
def home(request):
    destinations = {
        User.Role.ADMIN: "dashboards:admin",
        User.Role.MEDICO: "dashboards:medico",
        User.Role.RECEPCAO: "dashboards:recepcao",
        User.Role.PACIENTE: "dashboards:paciente",
    }
    destination = destinations.get(request.user.role)
    if not destination:
        raise Http404("Perfil de usuário inválido.")
    return redirect(destination)


def _dashboard(request, title):
    return render(request, "dashboards/dashboard.html", {"title": title})


@login_required
@roles_required(User.Role.ADMIN)
def admin_dashboard(request):
    return render(request, "dashboards/admin.html", admin_dashboard_data())


@login_required
@roles_required(User.Role.MEDICO)
def medico_dashboard(request):
    if not hasattr(request.user, "medico"):
        return _dashboard(request, "Dashboard médica — perfil profissional pendente")
    from medicos.views import medical_dashboard

    return medical_dashboard(request)


@login_required
@roles_required(User.Role.RECEPCAO)
def recepcao_dashboard(request):
    from recepcao.views import operational_dashboard

    return operational_dashboard(request)


@login_required
@roles_required(User.Role.PACIENTE)
def paciente_dashboard(request):
    patient = Paciente.objects.filter(user=request.user).first()
    if not patient:
        return _dashboard(request, "Dashboard do paciente — perfil pendente")
    return render(
        request, "dashboards/patient.html", patient_dashboard_data(patient=patient)
    )
