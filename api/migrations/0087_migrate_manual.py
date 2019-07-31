from django.db import migrations, transaction


def remove_pedidos(apps, schema_editor):
    Pedido = apps.get_model('api', 'Pedido')
    with transaction.atomic():
        Pedido.objects.all().delete()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('api', '0086_auto_20170730_2152'),
    ]

    operations = [
        migrations.RunPython(remove_pedidos),
    ]
