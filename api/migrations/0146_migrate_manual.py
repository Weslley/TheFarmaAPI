from django.db import migrations, transaction


def update_bairros(apps, schema_editor):
    Pedido = apps.get_model('api', 'Pedido')
    Bairro = apps.get_model('api', 'Bairro')
    with transaction.atomic():
        for pedido in Pedido.objects.all():
            if pedido.bairro:
                try:
                    bairro = Bairro.objects.filter(nome=pedido.bairro).first()
                    if bairro:
                        pedido._bairro = bairro
                        pedido.save()
                except Exception as err:
                    print(err)


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('api', '0145_pedido__bairro'),
    ]

    operations = [
        migrations.RunPython(update_bairros),
    ]
