# Generated by Django 3.2.9 on 2022-04-25 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_flagstart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flagstart',
            name='flag',
            field=models.BooleanField(default=True),
        ),
    ]
