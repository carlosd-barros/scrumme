from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Classe')),
                ('min_points', models.IntegerField(verbose_name='Minimos pontos')),
                ('max_points', models.IntegerField(blank=True, null=True, verbose_name='Maximo de pontos')),
                ('active', models.BooleanField(verbose_name='Ativo')),
            ],
            options={
                'verbose_name': 'Classe',
                'verbose_name_plural': 'Classes',
            },
        ),
        migrations.CreateModel(
            name='Jogador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nome Completo')),
                ('type', models.IntegerField(blank=True, choices=[(0, 'COMUM'), (1, 'SCRUM MASTER'), (2, 'PRODUCT OWNER')], default=0, null=True, verbose_name='Tipo de jogador')),
                ('points', models.IntegerField(default=0, verbose_name='Scrum points')),
                ('avatar', models.ImageField(default='profile_pics/default.svg', upload_to='profile_pics')),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Criado em')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Atualizado em')),
                ('classe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.Classe', verbose_name='Classe')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Jogador',
                'verbose_name_plural': 'Jogadores',
            },
        ),
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
                ('init_date', models.DateField(verbose_name='Inicio')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Fim')),
                ('points', models.IntegerField(verbose_name='Quantidade de pontos')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Criado em')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Atualizado em')),
                ('responsaveis', models.ManyToManyField(blank=True, to='core.Jogador', verbose_name='Responsáveis')),
            ],
            options={
                'verbose_name': 'Quest',
                'verbose_name_plural': 'Quests',
            },
        ),
        migrations.CreateModel(
            name='Equipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome da equipe')),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Criado em')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Atualizado em')),
                ('lider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lider', to='core.Jogador', verbose_name='Lider da equipe')),
                ('team', models.ManyToManyField(blank=True, related_name='team', to='core.Jogador', verbose_name='Time')),
            ],
            options={
                'verbose_name': 'Equipe',
                'verbose_name_plural': 'Equipes',
            },
        ),
    ]
