from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import User
from accounts.permissions import roles_required
from consultas.models import Consulta
from medicos.models import Medico
from pacientes.models import Paciente

from .forms import EvolucaoClinicaForm, ProntuarioForm
from .models import EvolucaoClinica, Prontuario
from .permissions import doctor_has_patient_link


def _doctor(user):
    return get_object_or_404(Medico, user=user, ativo=True)


@roles_required(User.Role.MEDICO)
@transaction.atomic
def record(request, consulta_id):
    medico = _doctor(request.user)
    consulta = get_object_or_404(
        Consulta.objects.select_related("paciente", "especialidade"),
        pk=consulta_id,
        medico=medico,
    )
    instance = Prontuario.objects.filter(consulta=consulta).first()
    from auditoria.services import log_action

    log_action(
        action="PRONTUARIO_ACESSADO", user=request.user, obj=instance or consulta
    )
    if request.method == "POST":
        form = ProntuarioForm(request.POST, instance=instance)
        if form.is_valid():
            prontuario = form.save(commit=False)
            prontuario.consulta, prontuario.paciente, prontuario.medico = (
                consulta,
                consulta.paciente,
                medico,
            )
            prontuario.full_clean()
            prontuario.save()
            log_action(action="PRONTUARIO_ALTERADO", user=request.user, obj=prontuario)
            messages.success(request, "Prontuário salvo com segurança.")
            return redirect("prontuarios:record", consulta_id=consulta.pk)
    else:
        form = ProntuarioForm(instance=instance)
    return render(
        request,
        "prontuarios/form.html",
        {
            "form": form,
            "consulta": consulta,
            "prontuario": instance,
            "evolution_form": EvolucaoClinicaForm(),
        },
    )


@require_POST
@roles_required(User.Role.MEDICO)
def add_evolution(request, consulta_id):
    medico = _doctor(request.user)
    prontuario = get_object_or_404(Prontuario, consulta_id=consulta_id, medico=medico)
    form = EvolucaoClinicaForm(request.POST)
    if form.is_valid():
        EvolucaoClinica.objects.create(
            prontuario=prontuario,
            medico=medico,
            descricao=form.cleaned_data["descricao"],
        )
        from auditoria.services import log_action

        log_action(action="EVOLUCAO_CLINICA_CRIADA", user=request.user, obj=prontuario)
        messages.success(request, "Evolução registrada.")
    return redirect("prontuarios:record", consulta_id=consulta_id)


@roles_required(User.Role.MEDICO)
def patient_history(request, paciente_id):
    medico = _doctor(request.user)
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    if not doctor_has_patient_link(medico=medico, paciente=paciente):
        return render(request, "403.html", status=403)
    records = (
        Prontuario.objects.filter(paciente=paciente)
        .select_related("consulta", "medico")
        .prefetch_related("evolucoes")
    )
    return render(
        request, "prontuarios/history.html", {"paciente": paciente, "records": records}
    )
