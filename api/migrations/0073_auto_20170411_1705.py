# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-11 17:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0072_auto_20170411_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartao',
            name='ano_expiracao',
            field=models.IntegerField(choices=[('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'), ('2031', '2031'), ('2032', '2032'), ('2033', '2033'), ('2034', '2034'), ('2035', '2035'), ('2036', '2036'), ('2037', '2037'), ('2038', '2038'), ('2039', '2039'), ('2040', '2040'), ('2041', '2041'), ('2042', '2042'), ('2043', '2043'), ('2044', '2044'), ('2045', '2045'), ('2046', '2046'), ('2047', '2047'), ('2048', '2048'), ('2049', '2049'), ('2050', '2050'), ('2051', '2051'), ('2052', '2052'), ('2053', '2053'), ('2054', '2054'), ('2055', '2055'), ('2056', '2056'), ('2057', '2057'), ('2058', '2058'), ('2059', '2059'), ('2060', '2060'), ('2061', '2061'), ('2062', '2062'), ('2063', '2063'), ('2064', '2064'), ('2065', '2065'), ('2066', '2066'), ('2067', '2067'), ('2068', '2068'), ('2069', '2069'), ('2070', '2070'), ('2071', '2071'), ('2072', '2072'), ('2073', '2073'), ('2074', '2074'), ('2075', '2075'), ('2076', '2076'), ('2077', '2077'), ('2078', '2078'), ('2079', '2079'), ('2080', '2080'), ('2081', '2081'), ('2082', '2082'), ('2083', '2083'), ('2084', '2084'), ('2085', '2085'), ('2086', '2086'), ('2087', '2087'), ('2088', '2088'), ('2089', '2089'), ('2090', '2090'), ('2091', '2091'), ('2092', '2092'), ('2093', '2093'), ('2094', '2094'), ('2095', '2095'), ('2096', '2096'), ('2097', '2097'), ('2098', '2098'), ('2099', '2099'), ('2100', '2100'), ('2101', '2101'), ('2102', '2102'), ('2103', '2103'), ('2104', '2104'), ('2105', '2105'), ('2106', '2106'), ('2107', '2107'), ('2108', '2108'), ('2109', '2109'), ('2110', '2110'), ('2111', '2111'), ('2112', '2112'), ('2113', '2113'), ('2114', '2114'), ('2115', '2115'), ('2116', '2116'), ('2117', '2117')], max_length=4),
        ),
        migrations.AlterField(
            model_name='cartao',
            name='mes_expiracao',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], max_length=2),
        ),
    ]
