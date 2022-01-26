# Generated by Django 3.0.7 on 2021-09-05 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20210905_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paymnet_status',
            field=models.CharField(choices=[('Unpaid', 'Unpaid'), ('Unconfirmend', 'Pending payment confirmation'), ('Recived', 'Payment Received')], default='Unpaid', max_length=120),
        ),
    ]