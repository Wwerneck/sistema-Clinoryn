from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import User
from accounts.permissions import roles_required
from consultas.models import Consulta
from medicos.models import Medico
from .forms import ItemFormSet, PrescricaoForm
from .models import Prescricao


@roles_required(User.Role.MEDICO, User.Role.PACIENTE)
def list_prescriptions(request):
    qs = Prescricao.objects.select_related(
        "paciente", "medico", "consulta"
    ).prefetch_related("itens")
    qs = (
        qs.filter(medico=getattr(request.user, "medico", None))
        if request.user.role == User.Role.MEDICO
        else qs.filter(paciente=getattr(request.user, "paciente", None))
    )
    return render(request, "prescricoes/list.html", {"prescriptions": qs})


@roles_required(User.Role.MEDICO)
@transaction.atomic
def create_prescription(request, consulta_id):
    medico = get_object_or_404(Medico, user=request.user)
    consulta = get_object_or_404(Consulta, pk=consulta_id, medico=medico)
    form, formset = (
        PrescricaoForm(request.POST or None),
        ItemFormSet(request.POST or None),
    )
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        obj = form.save(commit=False)
        obj.consulta, obj.paciente, obj.medico = consulta, consulta.paciente, medico
        obj.save()
        formset.instance = obj
        formset.save()
        from auditoria.services import log_action

        log_action(
            action="PRESCRICAO_CRIADA",
            user=request.user,
            obj=obj,
            metadata={"itens": obj.itens.count()},
        )
        return redirect("prescricoes:list")
    return render(
        request,
        "prescricoes/form.html",
        {"form": form, "formset": formset, "consulta": consulta},
    )
