# Generated by Django 5.1.2 on 2025-05-24 15:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_ingredient_product_is_gluten_free_product_is_halal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon_svg',
            field=models.TextField(blank=True, help_text="eg 'bx bxs-pizza'", null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.order'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_reference',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
