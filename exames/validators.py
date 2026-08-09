from pathlib import Path
from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
ALLOWED_MIMES = {"application/pdf", "image/jpeg", "image/png"}


def validate_medical_file(file):
    if Path(file.name).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValidationError("Formato não permitido.")
    if file.size > 10 * 1024 * 1024:
        raise ValidationError("O arquivo deve ter no máximo 10 MB.")
    content_type = getattr(file, "content_type", None)
    if content_type and content_type not in ALLOWED_MIMES:
        raise ValidationError("Tipo MIME não permitido.")
