# Generated by Django 3.0.7 on 2021-06-24 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_payment_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='timeStamp',
            new_name='payment_slip_upload_time',
        ),
    ]
