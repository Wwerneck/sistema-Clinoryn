import re

from django.core.exceptions import ValidationError


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def validate_cpf(value: str) -> None:
    cpf = only_digits(value)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValidationError("Informe um CPF válido.")
    for size in (9, 10):
        total = sum(int(cpf[index]) * (size + 1 - index) for index in range(size))
        digit = (total * 10 % 11) % 10
        if digit != int(cpf[size]):
            raise ValidationError("Informe um CPF válido.")


def validate_uf(value: str) -> None:
    if not re.fullmatch(r"[A-Z]{2}", value or ""):
        raise ValidationError("Informe a UF com duas letras maiúsculas.")
