# Generated by Django 3.0.7 on 2021-06-24 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20210625_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_slip',
            field=models.ImageField(upload_to='orders/paymentSlips'),
        ),
    ]
