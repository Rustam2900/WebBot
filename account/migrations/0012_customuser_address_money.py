# Generated by Django 4.2 on 2024-12-25 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_addressmoney_orderminsum'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address_money',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]