from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from .choices import JogadorType, JogadorClass


class Classe(models.Model):
    name = models.CharField("Nome", max_length=50)
    min_points = models.IntegerField("Pontos mínimos")
    max_points = models.IntegerField("Pontos máximos", blank=True, null=True)
    related_choice = models.IntegerField(
        "Classe choice relacionada",
        choices=JogadorClass.choices(),
        default=JogadorClass.INICIANTE.code,
        blank=True,
        null=True
    )
    active = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name='Classe'
        verbose_name_plural='Classes'

    def __str__(self):
        return self.name

class Jogador(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT
    )
    name = models.CharField(
        "Nome Completo",
        max_length=150,
    )
    classe = models.IntegerField(
        "Classe do jogador",
        choices=JogadorClass.choices(),
        default=JogadorClass.INICIANTE.code,
        blank=True,
        null=True
    )
    type = models.IntegerField(
        'Tipo de jogador',
        choices=JogadorType.choices(),
        default=JogadorType.COMUM.code,
        blank=True,
        null=True
    )
    points = models.IntegerField("Scrum points", default=0)
    avatar = models.FileField(
        null=True,
        blank=True,
        max_length=100,
        upload_to='profile_pics',
        verbose_name='Imagem do perfil',
        default='profile_pics/default.png',
        help_text='apenas imagens são aceitas'
    )
    active = models.BooleanField(default=True)
    created = models.DateTimeField("Criado em", auto_now_add=True, null=True)
    updated = models.DateTimeField('Atualizado em', auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if len(self.name) > 1:
            self.name = self.name.upper()
        else:
            self.name = self.user.username

        super(Jogador, self).save(*args, **kwargs)

    class Meta:
        verbose_name='Jogador'
        verbose_name_plural='Jogadores'

    def __str__(self):
        if self.name:
            return self.name
        return self.user.username


class Equipe(models.Model):
    name = models.CharField('Nome da equipe', max_length=100)
    lider = models.ForeignKey(
        Jogador,
        null=True,
        blank=True,
        verbose_name="Lider da equipe",
        related_name="lider",
        on_delete=models.PROTECT
    )
    team = models.ManyToManyField(
        Jogador,
        blank=True,
        verbose_name="Time",
        related_name="team"
    )
    active = models.BooleanField(default=True)
    created = models.DateTimeField("Criado em", auto_now_add=True, null=True)
    updated = models.DateTimeField('Atualizado em', auto_now=True, null=True)

    class Meta:
        verbose_name="Equipe"
        verbose_name_plural="Equipes"

    def __str__(self):
        return self.name


class Quest(models.Model):
    name = models.CharField("Nome", max_length=100)
    responsaveis = models.ManyToManyField(
        Jogador,
        blank=True,
        verbose_name="Responsáveis"
    )
    init_date = models.DateField("Inicio")
    end_date = models.DateField("Fim", null=True, blank=True)
    points = models.IntegerField("Quantidade de pontos")
    description = models.TextField("Descrição")
    active = models.BooleanField("Ativo", default=True)
    open = models.BooleanField("Concluida", default=True)
    created = models.DateTimeField("Criado em", auto_now_add=True, null=True)
    updated = models.DateTimeField("Atualizado em", auto_now=True, null=True)

    class Meta:
        verbose_name='Quest'
        verbose_name_plural='Quests'

    def __str__(self):
        return self.name