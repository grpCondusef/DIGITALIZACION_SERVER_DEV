# Generated by Django 4.1.2 on 2023-01-11 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CATALOGOS', '0020_alter_expediente_fechamodificacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente',
            name='resumenContenido',
            field=models.CharField(blank=True, max_length=1600, null=True),
        ),
    ]
