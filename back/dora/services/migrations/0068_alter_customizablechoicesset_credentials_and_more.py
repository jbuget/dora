# Generated by Django 4.0.6 on 2022-08-10 10:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0067_customizablechoicesset_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customizablechoicesset",
            name="credentials",
            field=models.ManyToManyField(
                blank=True,
                to="services.credential",
                verbose_name="Justificatifs à fournir ?",
            ),
        ),
        migrations.AlterField(
            model_name="customizablechoicesset",
            name="requirements",
            field=models.ManyToManyField(
                blank=True,
                to="services.requirement",
                verbose_name="Pré-requis ou compétences ?",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="customizable_choices_set",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="services.customizablechoicesset",
                verbose_name="Liste de choix",
            ),
        ),
    ]
