# Generated by Django 3.2.9 on 2022-04-25 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_alter_traplengh_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlagStart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag', models.BooleanField()),
            ],
        ),
    ]