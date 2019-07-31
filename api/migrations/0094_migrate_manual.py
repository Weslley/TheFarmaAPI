from django.db import migrations, transaction

from api.models.enums import StatusProduto


def update_produtos(apps, schema_editor):
    Produto = apps.get_model('api', 'Produto')
    with transaction.atomic():
        Produto.objects.update(status=StatusProduto.PUBLICADO)


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('api', '0093_auto_20170802_1503'),
    ]

    operations = [
        migrations.RunPython(update_produtos),
    ]
