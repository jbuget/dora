# Generated by Django 3.2.5 on 2021-07-26 15:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("structures", "0002_auto_20210715_0923"),
    ]

    operations = [
        migrations.RenameField(
            model_name="structure",
            old_name="has_solutions",
            new_name="has_services",
        ),
        migrations.AddField(
            model_name="structure",
            name="last_editor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
