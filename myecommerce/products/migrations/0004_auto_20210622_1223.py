# Generated by Django 3.0.7 on 2021-06-22 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_wishlist_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='whishlist_slug',
            field=models.CharField(max_length=42, unique=True),
        ),
    ]
