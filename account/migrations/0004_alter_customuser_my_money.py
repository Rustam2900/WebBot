# Generated by Django 4.2 on 2024-12-17 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_customuser_generate_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='my_money',
            field=models.DecimalField(decimal_places=15, default=0.0, max_digits=20),
        ),
    ]
