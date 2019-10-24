from django.db import models
from accounts.models import Jogador


class Equipe(models.Model):
    name = models.CharField('Nome da equipe', max_length=70)
    product_owner = models.ForeignKey(
        Jogador,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Product Owner",
        related_name='jogador_product_owner'
    )
    scrum_master = models.ForeignKey(
        Jogador,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Scrum Master",
        related_name='jogador_scrum_master'
    )
    dev_team = models.ManyToManyField(Jogador, verbose_name="Dev Team")
    active = models.BooleanField(default=True)
    created = models.DateTimeField("Criado em", auto_now_add=True, null=True)
    updated = models.DateTimeField('Atualizado em', auto_now=True, null=True)


    class Meta:
        verbose_name="Equipe"
        verbose_name_plural="Equipes"

    def __str__(self):
        return self.name
