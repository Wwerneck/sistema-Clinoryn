from typing import Any

from django.db import transaction

from .models import User


@transaction.atomic
def create_user_with_profile(*, role: str, profile_model, profile_data: dict[str, Any]) -> User:
    username = profile_data.pop("username")
    password = profile_data.pop("password")
    email = profile_data.get("email", "")
    full_name = profile_data.get("nome_completo") or profile_data.get("nome", "")
    first_name, _, last_name = full_name.partition(" ")
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=role,
    )
    profile_model.objects.create(user=user, **profile_data)
    return user
