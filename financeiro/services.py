from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import Pagamento


@transaction.atomic
def save_payment(*, consulta, forma_pagamento, status, actor):
    payment, _ = Pagamento.objects.select_for_update().get_or_create(
        consulta=consulta,
        defaults={
            "paciente": consulta.paciente,
            "medico": consulta.medico,
            "valor": consulta.valor,
            "forma_pagamento": forma_pagamento,
            "status": Pagamento.Status.PENDENTE,
            "registrado_por": actor,
        },
    )
    if payment.status == Pagamento.Status.ESTORNADO and status == Pagamento.Status.PAGO:
        raise ValidationError(
            "Pagamento estornado não pode voltar diretamente para pago."
        )
    payment.forma_pagamento, payment.status, payment.registrado_por = (
        forma_pagamento,
        status,
        actor,
    )
    payment.data_pagamento = timezone.now() if status == Pagamento.Status.PAGO else None
    payment.save()
    from auditoria.services import log_action

    log_action(
        action="PAGAMENTO_ALTERADO",
        user=actor,
        obj=payment,
        metadata={"status": status, "forma": forma_pagamento},
    )
    return payment
