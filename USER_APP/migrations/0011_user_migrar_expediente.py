# Generated by Django 4.1.2 on 2023-02-10 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('USER_APP', '0010_alter_user_consulta_completa_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='migrar_expediente',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
