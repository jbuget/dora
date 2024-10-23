# Generated by Django 3.2.5 on 2021-08-21 07:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0007_rename_location_kind_service_location_kinds"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="contact_email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="Courriel"
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="contact_name",
            field=models.CharField(
                blank=True, max_length=140, verbose_name="Nom du contact référent"
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="contact_phone",
            field=models.CharField(
                blank=True, max_length=10, verbose_name="Numéro de téléphone"
            ),
        ),
    ]
