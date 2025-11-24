from django.db import models
from django.contrib.auth.models import User

class InformacoesAdicionais(models.Model):
    cpf = models.CharField(max_length=14, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    dataNascimento = models.DateField(null=True, blank=True)
    tipoSanguineo = models.CharField(max_length=2, null=True, blank=True)
    alergiasMedicamentos = models.TextField(null=True, blank=True)
    restricoes = models.TextField(null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

class ContatosEmergencia(models.Model):
    nomeEmergencia = models.CharField(max_length=100, null=True, blank=True)
    telefoneEmergencia = models.CharField(max_length=15, null=True, blank=True)
    
    informacoes = models.OneToOneField(InformacoesAdicionais, on_delete=models.CASCADE, related_name="contatosemergencia")