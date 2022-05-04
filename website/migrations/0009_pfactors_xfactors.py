# Generated by Django 3.2.9 on 2022-04-11 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_rename_state_pairnorm_statenorm'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pfactors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField()),
                ('deltaP', models.FloatField()),
                ('expP', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Xfactors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField()),
                ('deltaX', models.FloatField()),
                ('expX', models.FloatField()),
            ],
        ),
    ]
