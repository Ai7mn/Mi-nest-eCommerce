# Generated by Django 3.0.7 on 2021-09-05 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210521_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='reciver_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
