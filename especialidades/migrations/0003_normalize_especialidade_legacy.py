from django.db import migrations


def normalize_legacy_specialty(apps, schema_editor):
    Especialidade = apps.get_model("especialidades", "Especialidade")
    Medico = apps.get_model("medicos", "Medico")
    Consulta = apps.get_model("consultas", "Consulta")

    oficial = Especialidade.objects.filter(nome__iexact="Psiquiatria").first()
    legado = Especialidade.objects.filter(nome__iexact="Psiquiatra").first()
    if not oficial or not legado or oficial.pk == legado.pk:
        return

    Medico.objects.filter(especialidade_id=legado.pk).update(
        especialidade_id=oficial.pk
    )
    Consulta.objects.filter(especialidade_id=legado.pk).update(
        especialidade_id=oficial.pk
    )
    legado.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("consultas", "0001_initial"),
        ("medicos", "0001_initial"),
        ("especialidades", "0002_seed_especialidades_cfm"),
    ]

    operations = [
        migrations.RunPython(
            normalize_legacy_specialty,
            migrations.RunPython.noop,
        ),
    ]
