from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import InformacoesAdicionais, ContatosEmergencia

@receiver(post_save, sender=User)
def criarInformacoes(sender, instance, created, **kwargs):
    if created:
        info = InformacoesAdicionais.objects.create(user=instance)
        ContatosEmergencia.objects.create(informacoes=info)