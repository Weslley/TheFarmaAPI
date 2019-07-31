from django.db import migrations, transaction


def update_pedidos(apps, schema_editor):
    Pedido = apps.get_model('api', 'Pedido')
    with transaction.atomic():
        Pedido.objects.update(latitude=0, longitude=0)


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('api', '0099_auto_20170809_0959'),
    ]

    operations = [
        migrations.RunPython(update_pedidos),
    ]
