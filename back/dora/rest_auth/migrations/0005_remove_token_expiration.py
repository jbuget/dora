# Generated by Django 4.1.9 on 2023-06-13 15:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("rest_auth", "0004_auto_20230613_1734"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="token",
            name="expiration",
        ),
    ]
