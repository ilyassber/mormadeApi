# Generated by Django 3.0.8 on 2020-08-09 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0015_product_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]