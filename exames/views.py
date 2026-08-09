from pathlib import Path
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import User
from accounts.permissions import roles_required
from consultas.models import Consulta
from medicos.models import Medico
from .forms import ExameForm
from .models import Exame


def _allowed(user, qs):
    return (
        qs.filter(medico=getattr(user, "medico", None))
        if user.role == User.Role.MEDICO
        else qs.filter(paciente=getattr(user, "paciente", None))
    )


@roles_required(User.Role.MEDICO, User.Role.PACIENTE)
def list_exams(request):
    return render(
        request,
        "exames/list.html",
        {
            "exams": _allowed(
                request.user, Exame.objects.select_related("paciente", "medico")
            )
        },
    )


@roles_required(User.Role.MEDICO)
def create_exam(request, consulta_id):
    medico = get_object_or_404(Medico, user=request.user)
    consulta = get_object_or_404(Consulta, pk=consulta_id, medico=medico)
    form = ExameForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.consulta, obj.paciente, obj.medico = consulta, consulta.paciente, medico
        obj.save()
        from auditoria.services import log_action

        log_action(
            action="EXAME_REGISTRADO",
            user=request.user,
            obj=obj,
            metadata={"possui_arquivo": bool(obj.arquivo)},
        )
        return redirect("exames:list")
    return render(
        request, "shared/form.html", {"form": form, "title": "Registrar exame"}
    )


@roles_required(User.Role.MEDICO, User.Role.PACIENTE)
def download(request, pk):
    exam = get_object_or_404(
        _allowed(request.user, Exame.objects.all()), pk=pk, arquivo__isnull=False
    )
    from auditoria.services import log_action

    log_action(action="EXAME_DOWNLOAD", user=request.user, obj=exam)
    return FileResponse(
        exam.arquivo.open("rb"),
        as_attachment=True,
        filename=Path(exam.arquivo.name).name,
    )
