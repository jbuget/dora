# Generated by Django 4.2.10 on 2024-04-24 03:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("logs", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="actionlog",
            name="level",
            field=models.SmallIntegerField(
                blank=True,
                choices=[
                    (50, "CRITICAL"),
                    (40, "ERROR"),
                    (30, "WARNING"),
                    (20, "INFO"),
                    (10, "DEBUG"),
                    (0, "NOTSET"),
                ],
                editable=False,
                verbose_name="niveau de log",
            ),
        ),
    ]
