# Generated by Django 4.1.2 on 2023-02-24 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CATALOGOS', '0031_alter_alfrescocca_foliosio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente',
            name='fechaCreacion',
            field=models.DateTimeField(blank=True),
        ),
    ]
