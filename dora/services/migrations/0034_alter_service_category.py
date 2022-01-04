# Generated by Django 3.2.11 on 2022-01-04 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0033_alter_service_kinds"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("MO", "Mobilité"),
                    ("HO", "Logement – Hébergement"),
                    ("CC", "Garde d’enfant"),
                    ("FL", "Apprendre le Français"),
                    ("IL", "Illettrisme"),
                    ("CR", "Création d’activité"),
                    ("DI", "Numérique"),
                    ("FI", "Difficultés financières"),
                    ("GL", "Acco. global individualisé"),
                ],
                db_index=True,
                max_length=2,
                verbose_name="Catégorie principale",
            ),
        ),
    ]
