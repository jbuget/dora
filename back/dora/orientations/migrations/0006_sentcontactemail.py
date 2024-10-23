# Generated by Django 4.2.3 on 2023-07-17 10:12

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orientations", "0005_create_rejection_reasons"),
    ]

    operations = [
        migrations.CreateModel(
            name="SentContactEmail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_sent", models.DateTimeField(auto_now_add=True)),
                (
                    "recipient",
                    models.CharField(
                        choices=[
                            ("BÉNÉFICIAIRE", "Bénéficiaire"),
                            ("PRESCRIPTEUR", "Prescripteur"),
                            ("RÉFÉRENT", "Référent"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "carbon_copies",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("BÉNÉFICIAIRE", "Bénéficiaire"),
                                ("PRESCRIPTEUR", "Prescripteur"),
                                ("RÉFÉRENT", "Référent"),
                            ],
                            max_length=20,
                        ),
                        blank=True,
                        default=list,
                        size=None,
                        verbose_name="Carbon Copies",
                    ),
                ),
                (
                    "orientation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="orientations.orientation",
                    ),
                ),
            ],
        ),
    ]
