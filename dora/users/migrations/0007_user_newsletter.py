# Generated by Django 3.2.8 on 2021-11-25 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_auto_20211008_1539"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="newsletter",
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
