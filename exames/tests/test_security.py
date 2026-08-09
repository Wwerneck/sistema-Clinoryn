from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from exames.validators import validate_medical_file


class UploadValidationTests(TestCase):
    def test_rejects_executable_extension(self):
        file = SimpleUploadedFile(
            "resultado.exe", b"content", content_type="application/octet-stream"
        )
        with self.assertRaises(ValidationError):
            validate_medical_file(file)

    def test_accepts_pdf(self):
        file = SimpleUploadedFile(
            "resultado.pdf", b"%PDF-1.4", content_type="application/pdf"
        )
        validate_medical_file(file)
