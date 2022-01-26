# Generated by Django 3.0.7 on 2021-05-21 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default='ABC', max_length=120, unique=True)),
                ('status', models.CharField(choices=[('Started', 'Started'), ('Abandoned', 'Abandoned'), ('Finished', 'Finished')], default='Started', max_length=120)),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('payment_slip', models.ImageField(blank=True, null=True, upload_to='orders/paymentSlips')),
                ('paymnet_status', models.CharField(choices=[('Unpaid', 'Unpaid'), ('Unconfirmend', 'Unconfirmend'), ('Recived', 'Recived')], default='Unpaid', max_length=120)),
                ('courier_company', models.CharField(blank=True, max_length=120, null=True)),
                ('payment_slip_uploaded_at', models.DateTimeField(blank=True, null=True)),
                ('tax_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('final_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.UserAddress')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.Cart')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]