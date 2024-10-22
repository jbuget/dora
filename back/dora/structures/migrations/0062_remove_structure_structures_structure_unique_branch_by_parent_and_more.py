# Generated by Django 4.2.3 on 2023-09-07 09:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0061_structure_disable_orientation_form"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="structure",
            name="structures_structure_unique_branch_by_parent",
        ),
        migrations.RemoveConstraint(
            model_name="structure",
            name="structures_structure_branches_have_id",
        ),
        migrations.RemoveField(
            model_name="structure",
            name="branch_id",
        ),
    ]
