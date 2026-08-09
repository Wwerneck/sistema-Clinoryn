from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from accounts.permissions import roles_required
from consultas.models import Consulta

from .forms import PagamentoForm
from .selectors import financial_summary, payments_for_user
from .services import save_payment


@roles_required(
    User.Role.ADMIN, User.Role.RECEPCAO, User.Role.MEDICO, User.Role.PACIENTE
)
def dashboard(request):
    payments = payments_for_user(request.user)
    return render(
        request,
        "financeiro/dashboard.html",
        {"payments": payments, "summary": financial_summary(payments)},
    )


@roles_required(User.Role.ADMIN, User.Role.RECEPCAO)
def register_payment(request, consulta_id):
    consulta = get_object_or_404(
        Consulta.objects.select_related("paciente", "medico"), pk=consulta_id
    )
    existing = getattr(consulta, "pagamento", None)
    form = PagamentoForm(request.POST or None, instance=existing)
    if request.method == "POST" and form.is_valid():
        save_payment(
            consulta=consulta,
            forma_pagamento=form.cleaned_data["forma_pagamento"],
            status=form.cleaned_data["status"],
            actor=request.user,
        )
        messages.success(request, "Pagamento registrado com sucesso.")
        return redirect("financeiro:dashboard")
    return render(
        request,
        "shared/form.html",
        {"form": form, "title": f"Pagamento — {consulta.paciente.nome_completo}"},
    )
