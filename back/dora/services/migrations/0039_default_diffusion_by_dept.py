# Generated by Django 3.2.12 on 2022-02-25 10:19

from django.db import migrations

from dora.admin_express.models import AdminDivisionType
from dora.core.utils import code_insee_to_code_dept


def set_default_diffusion_zone(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    for service in Service.objects.all():
        # On ne veut pas changer la zone de diffusion pour le CD 974
        if service.structure.siret != "22974001400019":
            diffusion_zone_type = AdminDivisionType.DEPARTMENT
            if service.city_code:
                diffusion_zone_details = code_insee_to_code_dept(service.city_code)
            elif service.structure.city_code:
                diffusion_zone_details = code_insee_to_code_dept(
                    service.structure.city_code
                )
            else:
                print("missing diffusion zone:", service.slug)
                diffusion_zone_details = ""
            # On ne veut pas mettre à jour la date de modification
            Service.objects.filter(pk=service.pk).update(
                diffusion_zone_type=diffusion_zone_type,
                diffusion_zone_details=diffusion_zone_details,
            )


def noop(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    Service.objects.update(diffusion_zone_details="", diffusion_zone_type="")


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0038_alter_service_diffusion_zone_type"),
    ]

    operations = [
        migrations.RunPython(set_default_diffusion_zone, noop),
    ]
