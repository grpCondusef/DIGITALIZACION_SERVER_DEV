# Generated by Django 4.1.2 on 2022-11-24 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CATALOGOS', '0009_expediente_idestatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipodocumental',
            name='tipo_macroproceso',
            field=models.ManyToManyField(to='CATALOGOS.tipomacroproceso'),
        ),
    ]
