# Generated by Django 5.0.6 on 2024-07-09 09:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0005_remove_orderitem_unit_price"),
        ("products", "0003_alter_product_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="unit_price",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="products.price",
            ),
        ),
    ]