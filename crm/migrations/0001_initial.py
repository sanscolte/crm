# Generated by Django 5.0.4 on 2024-04-08 21:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Campaign",
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
                ("name", models.CharField(max_length=100, verbose_name="название")),
                (
                    "promotion_channel",
                    models.CharField(max_length=100, verbose_name="канал продвижения"),
                ),
                (
                    "budget",
                    models.DecimalField(decimal_places=2, max_digits=10, verbose_name="бюджет"),
                ),
            ],
            options={
                "verbose_name": "Рекламная компания",
                "verbose_name_plural": "Рекламные компании",
            },
        ),
        migrations.CreateModel(
            name="Contract",
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
                ("name", models.CharField(max_length=100, verbose_name="название")),
                (
                    "document",
                    models.FileField(upload_to="documents/", verbose_name="документ"),
                ),
                ("conclusion_date", models.DateField(verbose_name="дата заключения")),
                (
                    "validity_period",
                    models.PositiveIntegerField(verbose_name="период действия"),
                ),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, max_digits=10, verbose_name="сумма"),
                ),
            ],
            options={
                "verbose_name": "Контракт",
                "verbose_name_plural": "Контракты",
            },
        ),
        migrations.CreateModel(
            name="Service",
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
                ("name", models.CharField(max_length=100, verbose_name="название")),
                ("description", models.TextField(verbose_name="описание")),
                (
                    "cost",
                    models.DecimalField(decimal_places=2, max_digits=100, verbose_name="стоимость"),
                ),
            ],
            options={
                "verbose_name": "Услуга",
                "verbose_name_plural": "Услуги",
            },
        ),
        migrations.CreateModel(
            name="PotentialClient",
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
                ("full_name", models.CharField(max_length=100, verbose_name="Ф.И.О")),
                ("phone", models.CharField(max_length=11, verbose_name="телефон")),
                ("email", models.EmailField(max_length=254, verbose_name="email")),
                (
                    "campaign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crm.campaign",
                        verbose_name="рекламная кампания",
                    ),
                ),
            ],
            options={
                "verbose_name": "Потенциальный клиент",
                "verbose_name_plural": "Потенциальные клиенты",
            },
        ),
        migrations.CreateModel(
            name="ActiveClient",
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
                    "contract",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crm.contract",
                        verbose_name="контракт",
                    ),
                ),
                (
                    "potential_client",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crm.potentialclient",
                        verbose_name="потенциальный клиент",
                    ),
                ),
            ],
            options={
                "verbose_name": "Активный клиент",
                "verbose_name_plural": "Активные клиенты",
            },
        ),
        migrations.AddField(
            model_name="contract",
            name="service",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="crm.service",
                verbose_name="услуга",
            ),
        ),
        migrations.AddField(
            model_name="campaign",
            name="service",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="crm.service",
                verbose_name="услуга",
            ),
        ),
    ]
