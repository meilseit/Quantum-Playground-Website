# Generated by Django 3.2.9 on 2022-03-30 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_pairnorm'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pairnorm',
            old_name='state',
            new_name='stateNorm',
        ),
    ]
