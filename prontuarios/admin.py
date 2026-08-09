from django.contrib import admin
from .models import EvolucaoClinica, Prontuario

admin.site.register(Prontuario)
admin.site.register(EvolucaoClinica)
