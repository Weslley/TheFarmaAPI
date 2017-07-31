from django.db import migrations, transaction


def remove_farmacias(apps, schema_editor):
    Farmacia = apps.get_model('api', 'Farmacia')
    with transaction.atomic():
        Farmacia.objects.all().delete()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('api', '0087_migrate_manual'),
    ]

    operations = [
        migrations.RunPython(remove_farmacias),
    ]
