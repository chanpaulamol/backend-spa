# Generated by Django 4.2.1 on 2023-05-16 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SupplierManagementApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ahpcalculation',
            name='results',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]