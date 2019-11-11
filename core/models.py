from django.db import models
from .choices import JogadorType
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Classe(models.Model):
    name = models.CharField("Classe", max_length=50)
    min_points = models.IntegerField("Minimos pontos")
    max_points = models.IntegerField("Maximo de pontos", blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    active = models.BooleanField('Ativo')

    def save(self, **kwargs):
        if self.name:
            self.slug = slugify(self.name)

        super(Classe, self).save(**kwargs)

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
    classe = models.ForeignKey(
        Classe,
        null=True,
        blank=True,
        verbose_name="Classe",
        on_delete=models.PROTECT
    )
    type = models.IntegerField(
        'Tipo de jogador',
        choices=JogadorType.choices(),
        default=JogadorType.COMUM.code,
        blank=True,
        null=True
    )
    points = models.IntegerField("Scrum points", default=0)
    avatar = models.ImageField(default='profile_pics/default.svg', upload_to='profile_pics')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField("Criado em", auto_now_add=True, null=True)
    updated = models.DateTimeField('Atualizado em', auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.upper()
        else:
            self.name = self.user.username

        self.slug = slugify(self.name)

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
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField("Criado em", auto_now_add=True, null=True)
    updated = models.DateTimeField('Atualizado em', auto_now=True, null=True)

    def save(self, **kwargs):
        if self.name:
            self.slug = slugify(self.name)

        super(Equipe, self).save(**kwargs)
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
        verbose_name="Responsáveis",
    )
    init_date = models.DateField("Inicio")
    end_date = models.DateField("Fim", null=True, blank=True)
    points = models.IntegerField("Quantidade de pontos")
    description = models.TextField("Descrição")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    active = models.BooleanField("Ativo", default=True)
    created = models.DateTimeField("Criado em", auto_now_add=True, null=True)
    updated = models.DateTimeField("Atualizado em", auto_now=True, null=True)

    def save(self, **kwargs):
        if self.name:
            self.slug = slugify(self.name)
        
        super(Quest, self).save(**kwargs)

    class Meta:
        verbose_name='Quest'
        verbose_name_plural='Quests'

    def __str__(self):
        return self.name