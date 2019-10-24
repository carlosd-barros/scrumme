from django.db import models
from django.contrib.auth.models import User


class Jogador(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    name = models.CharField("Nome Completo", default='', max_length=150, null=True, blank=True)
    image = models.ImageField(default='profile01.svg', upload_to='profile_pics')
    active = models.BooleanField(default=True)
    created = models.DateTimeField("Criado em", auto_now_add=True, null=True)
    updated = models.DateTimeField('Atualizado em', auto_now=True, null=True)

    class Meta:
        verbose_name='Pessoa'
        verbose_name_plural='Pessoas'

    def __str__(self):
        return self.name
