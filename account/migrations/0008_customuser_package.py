# Generated by Django 4.2 on 2024-12-24 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_vippackage_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='package',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.vippackage'),
            preserve_default=False,
        ),
    ]