# Generated by Django 3.2.5 on 2021-08-21 07:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0008_auto_20210813_1726"),
    ]

    operations = [
        migrations.AlterField(
            model_name="structure",
            name="email",
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]