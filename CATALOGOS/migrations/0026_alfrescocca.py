# Generated by Django 4.1.2 on 2023-02-09 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CATALOGOS', '0025_alter_expediente_idinstitucion'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlfrescoCCA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave', models.CharField(max_length=250)),
            ],
        ),
    ]
