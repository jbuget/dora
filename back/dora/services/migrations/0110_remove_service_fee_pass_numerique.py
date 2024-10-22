# Generated by Django 4.2.15 on 2024-08-28 14:24

from django.db import migrations


def delete_pass_numerique(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    ServiceFee = apps.get_model("services", "ServiceFee")

    Service.objects.filter(fee_condition__value="pass-numerique").update(
        fee_condition=None
    )
    ServiceFee.objects.get(value="pass-numerique").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0109_rename_orientation_mode_labels"),
    ]

    operations = [
        migrations.RunPython(
            delete_pass_numerique, reverse_code=migrations.RunPython.noop
        ),
    ]
