# Generated by Django 4.2 on 2024-12-22 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_remove_customuser_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='vippackage',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.customuser'),
            preserve_default=False,
        ),
    ]