# Generated by Django 5.0.6 on 2024-07-08 08:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_alter_blog_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="products",
                to="catalog.category",
                verbose_name="Категория",
            ),
        ),
        migrations.CreateModel(
            name="Version",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "version_number",
                    models.PositiveIntegerField(
                        blank=True,
                        default=1,
                        help_text="Введите номер версии продукта",
                        null=True,
                        verbose_name="Номер версии",
                    ),
                ),
                (
                    "name_version",
                    models.CharField(
                        blank=True,
                        help_text="Введите название версии продукта",
                        max_length=100,
                        null=True,
                        verbose_name="Название версии",
                    ),
                ),
                (
                    "current_version",
                    models.BooleanField(
                        default=True,
                        help_text="Отметьте, является ли текущей версией продукта актуальной",
                        verbose_name="Текущая версия",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="catalog.product",
                        verbose_name="Продукты",
                    ),
                ),
            ],
            options={
                "verbose_name": "Версия продукта",
                "verbose_name_plural": "Версии продуктов",
            },
        ),
    ]
