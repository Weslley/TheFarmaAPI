# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-20 23:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20160817_0830'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apresentacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_barras', models.BigIntegerField(blank=True, null=True)),
                ('nome', models.CharField(blank=True, max_length=60, null=True)),
                ('registro_ms', models.CharField(blank=True, max_length=17, null=True)),
                ('imagem', models.ImageField(upload_to='apresentacoes')),
            ],
        ),
        migrations.CreateModel(
            name='Bairro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(blank=True, max_length=8, null=True)),
                ('logradouro', models.CharField(max_length=80)),
                ('numero', models.IntegerField(blank=True, null=True)),
                ('complemento', models.CharField(blank=True, max_length=10, null=True)),
                ('bairro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Bairro')),
            ],
            options={
                'verbose_name_plural': 'Endereços',
                'verbose_name': 'Endereço',
            },
        ),
        migrations.CreateModel(
            name='RepresentanteLegal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
                ('rg', models.CharField(blank=True, max_length=14, null=True, verbose_name='RG')),
                ('cpf', models.CharField(max_length=11, verbose_name='CPF')),
                ('telefone', models.CharField(max_length=11)),
                ('endereco', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Endereco')),
            ],
            options={
                'verbose_name_plural': 'Representantes legais',
                'verbose_name': 'Representante legal',
            },
        ),
        migrations.CreateModel(
            name='TabelaPreco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icm', models.DecimalField(decimal_places=2, max_digits=15)),
                ('pmc', models.DecimalField(decimal_places=2, max_digits=15)),
                ('pmf', models.DecimalField(decimal_places=2, max_digits=15)),
                ('data_vigencia', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Tabela de preços',
                'verbose_name': 'Tabela de preço',
            },
        ),
        migrations.CreateModel(
            name='Uf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigla', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2)),
                ('nome', models.CharField(max_length=20)),
                ('tabela_preco', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.TabelaPreco')),
            ],
        ),
        migrations.RemoveField(
            model_name='grupomedicamento',
            name='principio_ativo',
        ),
        migrations.AlterModelOptions(
            name='farmacia',
            options={'verbose_name': 'Farmácia', 'verbose_name_plural': 'Farmácias'},
        ),
        migrations.AlterModelOptions(
            name='medicamento',
            options={},
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='bairro',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='bairro_responsavel',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='cep',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='cep_responsavel',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='cidade',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='cidade_responsavel',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='complemento',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='complemento_responsavel',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='cpf_responsavel',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='logradouro',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='logradouro_responsavel',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='nome_responsavel',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='numero',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='numero_responsavel',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='rg_responsavel',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='sobrenome_responsavel',
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='telefone_responsavel',
        ),
        migrations.RemoveField(
            model_name='medicamento',
            name='codigo_barras',
        ),
        migrations.RemoveField(
            model_name='medicamento',
            name='generico',
        ),
        migrations.RemoveField(
            model_name='medicamento',
            name='grupo',
        ),
        migrations.RemoveField(
            model_name='medicamento',
            name='nome_complementar',
        ),
        migrations.RemoveField(
            model_name='medicamento',
            name='preco_maximo',
        ),
        migrations.RemoveField(
            model_name='medicamento',
            name='registro',
        ),
        migrations.AddField(
            model_name='farmacia',
            name='logo',
            field=models.ImageField(default='', upload_to='farmacias'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cidade',
            name='uf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Uf'),
        ),
        migrations.AlterField(
            model_name='medicamento',
            name='tipo',
            field=models.IntegerField(choices=[(0, 'GENÉRICO'), (1, 'SIMILAR'), (2, 'ÉTICO')]),
        ),
        migrations.DeleteModel(
            name='GrupoMedicamento',
        ),
        migrations.AddField(
            model_name='representantelegal',
            name='farmacia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='representantes', to='api.Farmacia'),
        ),
        migrations.AddField(
            model_name='endereco',
            name='cidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Cidade'),
        ),
        migrations.AddField(
            model_name='bairro',
            name='cidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Cidade'),
        ),
        migrations.AddField(
            model_name='apresentacao',
            name='medicamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apresentacoes', to='api.Medicamento'),
        ),
        migrations.AddField(
            model_name='apresentacao',
            name='tabela',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apresentacoes', to='api.TabelaPreco'),
        ),
        migrations.AddField(
            model_name='farmacia',
            name='endereco',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='api.Endereco'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='endereco',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='api.Endereco'),
            preserve_default=False,
        ),
    ]
