# Generated by Django 2.2.5 on 2019-11-05 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jogador',
            name='avatar',
            field=models.ImageField(default='profile_pics/default.svg', upload_to='profile_pics'),
        ),
    ]