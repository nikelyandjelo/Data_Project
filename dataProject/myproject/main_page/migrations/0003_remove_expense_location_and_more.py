# Generated by Django 4.1.6 on 2023-05-23 07:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main_page", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="expense", name="location",),
        migrations.RemoveField(model_name="income", name="income_payment_method",),
        migrations.AddField(
            model_name="expense",
            name="currency",
            field=models.CharField(
                choices=[("USD", "USD"), ("EUR", "EUR"), ("GBP", "GBP")],
                default="",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="expense",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="income",
            name="currency",
            field=models.CharField(
                choices=[("USD", "USD"), ("EUR", "EUR"), ("GBP", "GBP")],
                default="",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="income",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="expense", name="description", field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="expense",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("Cash", "Cash"),
                    ("Credit Card", "Credit Card"),
                    ("Bank Transfer", "Bank Transfer"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="income", name="description", field=models.TextField(),
        ),
        migrations.DeleteModel(name="IncomePaymentMethod",),
        migrations.DeleteModel(name="Location",),
        migrations.DeleteModel(name="PaymentMethod",),
    ]