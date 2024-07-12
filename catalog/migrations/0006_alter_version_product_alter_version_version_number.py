# Generated by Django 4.2 on 2024-07-09 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_alter_product_category_version"),
    ]

    operations = [
        migrations.AlterField(
            model_name="version",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="versions",
                to="catalog.product",
                verbose_name="Продукты",
            ),
        ),
        migrations.AlterField(
            model_name="version",
            name="version_number",
            field=models.PositiveIntegerField(
                default=1,
                help_text="Введите номер версии продукта",
                verbose_name="Номер версии",
            ),
        ),
    ]
